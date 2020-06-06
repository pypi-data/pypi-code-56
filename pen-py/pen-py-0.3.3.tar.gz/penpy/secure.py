import hashlib
import json
import os
import socket
import time
import uuid
from base64 import b64encode
from calendar import timegm
from datetime import datetime, timedelta
from functools import wraps

import requests
from jose import jwk, jws, jwt

from flask import g, request

from .dicplus import DicPlus

ALGORITHMS = ["RS256"]
EXPIRATION = 1000


class AuthError(Exception):
    status_code = 500


def hash_digest(body):
    myhash = hashlib.sha512()
    myhash.update(body)
    digest = b64encode(myhash.digest()).decode()
    return digest


def get_token_header(auth_type, request):
    """Obtains the Access Token from the Authorization Header
    """
    auth = request.headers.get("Authorization", None)
    if not auth:
        raise AuthError("No Authorization Header")

    auth_parts = auth.split()

    if auth_parts[0].lower() != auth_type.lower():
        raise AuthError("Authorization Header must start with {}".format(auth_type))
    elif len(auth_parts) == 1:
        raise AuthError("No Signature attached")
    elif len(auth_parts) > 2:
        raise AuthError("Invalid Header")
    token = auth_parts[1]

    return token


def make_keySet(keySet, issuers):
    myKeySet = KeySet()
    for k in keySet:
        if k["issuer"] in issuers:
            myKeySet.add_issuer(
                issuer=k["issuer"], keys=k["keys"] if "keys" in k else None
            )
    return myKeySet


class Secure:
    def __init__(
        self,
        service,
        keySet=None,
        auth_makers=[],
        auth_checkers=[],
        sign_makers=[],
        sign_checkers=[],
    ):
        self.service = service
        self.keySet = keySet
        self.auth_makers = {}
        self.auth_checkers = {}
        self.sign_makers = {}
        self.sign_checkers = {}
        if len(auth_makers) > 0:
            for k, v in auth_makers.items():
                if v["type"] == "auth0":
                    config = v["config"]
                    config["domain"] = "https://{}/oauth/token".format(config["domain"])
                    self.auth_makers[k] = Authenticator(**config)
                else:
                    self.auth_makers[k] = Authenticator(**v["config"])
        if len(auth_checkers) > 0:
            for k, v in auth_checkers.items():
                self.auth_checkers[k] = Authorizer(
                    audience=v["audience"], keySet=make_keySet(keySet, v["issuers"])
                )
        if len(sign_makers) > 0:
            for k, v in sign_makers.items():
                self.sign_makers[k] = Signer(
                    issuer=v["issuer"], private_key=v["private_key"]
                )
        if len(sign_checkers) > 0:
            for k, v in sign_checkers.items():
                self.sign_checkers[k] = Signature_Verifyer(
                    audience=v["audience"], keySet=make_keySet(keySet, v["issuers"])
                )

    def validate_scope(self, scope, token=None):
        try:
            token_payload = jwt.get_unverified_claims(token)
        except:
            raise AuthError("Error in token access")
        if scope == None or scope == "":
            return True
        if token_payload.get("scope"):
            scope = scope.split()
            for s in scope:
                if s not in token_payload["scope"]:
                    return False
        return True

    def auth_check(self, name=None, scope=None, issuers=None):
        def inner_auth_check(f):
            @wraps(f)
            def decorated(*args, **kwargs):
                try:
                    if len(self.auth_checkers) == 1:
                        auth_checker = next(iter(self.auth_checkers.values()))
                    elif len(self.auth_checkers) > 1:
                        auth_checker = self.auth_checkers[name]
                    else:
                        raise AuthError("No Auth Checker defined in Config")
                    token = get_token_header("Bearer", request)
                    payload = auth_checker.decode(token, issuers)
                except:
                    raise AuthError("Invalid Bearer Token")
                if not self.validate_scope(scope, token):
                    raise AuthError("Invalid Scope")
                return f(*args, **kwargs)

            return decorated

        return inner_auth_check

    def auth_headers(self, name=None):
        headers = {"Authorization": "Bearer {}".format(self.get_access_token(name))}
        return headers

    def get_access_token(self, name=None):
        if len(self.auth_makers) == 1:
            auth_maker = next(iter(self.auth_makers.values()))
        elif len(self.auth_makers) > 1:
            auth_maker = self.auth_makers[name]
        else:
            raise AuthError("No Auth Maker defined in Config")
        return auth_maker.access_token

    def sign_check(self, name=None, json_dec=False, issuers=None):
        def inner_sign_check(f):
            @wraps(f)
            def decorated(*args, **kwargs):
                if len(self.sign_checkers) == 1:
                    sign_checker = next(iter(self.sign_checkers.values()))
                elif len(self.auth_checkers) > 1:
                    sign_checker = self.sign_checkers[name]
                else:
                    raise AuthError("No Sign Checker defined in Config")
                # Assumes the request is available
                token = get_token_header("signature", request)
                body = request.get_data()
                if not sign_checker.verify(token, body, json_dec, issuers):
                    raise AuthError("Wrong Signature", 401)

                return f(*args, **kwargs)

            return decorated

        return inner_sign_check

    def auth_or_sign_check(self, scope=None, name=None, json_dec=False, issuers=None):
        def inner_auth_or_sign_check(f):
            @wraps(f)
            def decorated(*args, **kwargs):
                auth = request.headers.get("Authorization", None)
                if not auth:
                    raise AuthError("No Authorization Header")

                auth_parts = auth.split()

                if auth_parts[0].lower() not in ["signature", "bearer"]:
                    raise AuthError("Header should start Bearer or Signature")
                elif len(auth_parts) == 1:
                    raise AuthError("No Token attached")
                elif len(auth_parts) > 2:
                    raise AuthError("Too many parts in Token")
                token = auth_parts[1]
                auth_type = auth_parts[0].lower()
                if auth_type == "signature":
                    if len(self.sign_checkers) == 1:
                        sign_checker = next(iter(self.sign_checkers.values()))
                    elif len(self.auth_checkers) > 1:
                        sign_checker = self.sign_checkers[name]
                    else:
                        raise AuthError("No Sign Checker defined in Config")
                    # Assumes the request is available
                    body = request.get_data()
                    if not sign_checker.verify(token, body, json_dec, issuers):
                        raise AuthError("Signature can't validate Body")

                elif auth_type == "bearer":
                    if len(self.auth_checkers) == 1:
                        auth_checker = next(iter(self.auth_checkers.values()))
                    elif len(self.auth_checkers) > 1:
                        auth_checker = self.auth_checkers[name]
                    else:
                        raise AuthError("No Auth Checker defined in Config")
                    auth_checker.decode(token, issuers)
                    if not self.validate_scope(scope, token):
                        raise AuthError("Invalid Scope")

                return f(*args, **kwargs)

            return decorated

        return inner_auth_or_sign_check

    def sign_make(self, body, audience, name=None, is_binary=False):
        if len(self.sign_makers) == 1:
            sign_maker = next(iter(self.sign_makers.values()))
        elif len(self.sign_makers) > 1:
            sign_maker = self.sign_makers[name]
        else:
            raise AuthError("No Sign Maker defined in Config")
        return sign_maker.sign(body, audience, is_binary)

    def signed_headers(self, body, audience, name=None, is_binary=False):
        headers = {
            "Authorization": "Signature {}".format(
                self.sign_make(body, audience, name, is_binary)
            )
        }
        return headers


class KeySet:
    def __init__(self, jsonfile=None):
        self.issuers = []
        if jsonfile:
            self.from_json(jsonfile)

    def add_issuer(self, issuer, keys=None):
        if not keys:
            try:
                url = issuer + ".well-known/jwks.json"
                keys = requests.get(url=url).json()["keys"]
            except:
                raise AuthError(
                    "No keys provided nor found on {}.well-known/jwks.json".format(
                        issuer
                    )
                )
        if type(keys) != list:
            keys = [keys]
        self.issuers.append({"issuer": issuer, "keys": keys})

    def from_json(self, jsonfile):
        dp = DicPlus.from_json(jsonfile)
        for ks in dp.keySet:
            issuer = ks.toDict()
            if "keys" not in ks:
                self.add_issuer(issuer["issuer"])
            else:
                self.add_issuer(issuer["issuer"], issuer["keys"])

    def get_keys(self, issuers=None):
        keys = []
        if not issuers:
            issuers = [i["issuer"] for i in self.issuers]
        if type(issuers) != list and issuers is not None:
            issuers = [issuers]
        for i in self.issuers:
            if issuers:
                if i["issuer"] not in issuers:
                    continue
            for key in i["keys"]:
                keys.append(key)

        return {"keys": keys}


class Authenticator:
    # Using Auth0
    def __init__(
        self,
        domain,
        client_id,
        client_secret,
        audience,
        grant_type="client_credentials",
    ):
        self.domain = domain
        self.client_id = client_id
        self.client_secret = client_secret
        self.audience = audience
        self.getAccessToken()
        self.grant_type = grant_type
        if self._access_token is None:
            raise AuthError("Request for access token failed")

    def getAccessToken(self, scope=""):
        body = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "audience": self.audience,
            "grant_type": self.grant_type,
            "scope": scope,
        }
        try:
            response = requests.post(url=self.domain, json=body)
        except Exception as e:
            raise AuthError(e)
            return None
        else:
            json_response = DicPlus.json_loads(response.text)
            self._access_token = json_response.access_token
            self._access_token_expiration = time.time() + float(
                json_response.expires_in
            )

    @property
    def access_token(self, scope=""):
        if time.time() > self._access_token_expiration:
            self.getAccessToken(scope)
        return self._access_token


class Authorizer:
    def __init__(self, audience, keySet):
        self.audience = audience
        self.keySet = keySet

    def decode(self, token, issuers=None):
        try:
            jwks = self.keySet.get_keys(issuers)
            payload = jwt.decode(token, jwks, audience=self.audience)
        except jwt.ExpiredSignatureError:
            raise AuthError("Expired Signature", 401)
        except jwt.JWTClaimsError:
            raise AuthError("Please check audience and issuer", 401)
        except Exception as e:
            raise AuthError("Invalid Token", e)

        return payload


class Signature_Verifyer:
    def __init__(self, audience, keySet, jti_cache=None):

        self.jti_cache = jti_cache
        self.algorithms = ALGORITHMS
        self.audience = audience
        self.keySet = keySet

    def verify(self, token, body, json_dec=False, issuers=None):
        jwks = self.keySet.get_keys(issuers)
        verified_token = DicPlus(json.loads(jws.verify(token, jwks, self.algorithms)))
        if json_dec:
            dec_body = json.loads(body)
            enc_body = json.dumps(dec_body, separators=(",", ": ")).encode()
            hashed_body = hash_digest(enc_body)
        else:
            hashed_body = hash_digest(body)
        if verified_token.digest != hashed_body:
            raise AuthError("Digest Not Equal")
        if verified_token.aud != self.audience:
            raise AuthError("Audience Not Equal")
        if verified_token.exp < timegm(datetime.utcnow().utctimetuple()):
            raise AuthError("Token Expired")
        return True


class Signer:
    def __init__(
        self, issuer, private_key, algorithm=ALGORITHMS[0], expiration=EXPIRATION
    ):
        self.algorithm = algorithm
        self.expiration = expiration
        self.issuer = issuer
        self.private_key = private_key

    def sign(self, body, audience, is_binary=False):
        jti = str(uuid.uuid4())
        if is_binary:
            enc_body = body
        else:
            enc_body = json.dumps(body, separators=(",", ": ")).encode()
        digest = hash_digest(enc_body)
        print(digest)
        token_payload = {
            "digest": digest,
            "jti": jti,
            "iat": timegm(datetime.utcnow().utctimetuple()),
            "exp": timegm(datetime.utcnow().utctimetuple()) + self.expiration,
            "iss": self.issuer,
            "aud": audience,
        }
        signed_token = jws.sign(
            token_payload, self.private_key, algorithm=self.algorithm
        )

        return signed_token
