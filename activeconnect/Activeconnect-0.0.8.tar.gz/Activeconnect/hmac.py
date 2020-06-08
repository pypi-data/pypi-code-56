import base64
import datetime
import hashlib
import hmac
import re
import time
from os import urandom
from sys import byteorder


def make_authentication_headers(client_id: str, client_shared_secret: str, request_uri: str) -> dict:
    """ Makes a dictionary with authentication headers (used across all the services)
    using given secret keys.

    :param client_id:
    :param client_shared_secret:
    :param request_uri: URI that was used for encoding
    :return: headers dictionary
    """
    token, timestamp = encode_auth_token(client_id, client_shared_secret, request_uri)
    return {
        'Authentication': token,
        'X-Sonikpass-Authentication-Timestamp': str(timestamp),
        'X-Sonikpass-Authentication-Version': '1'
    }


def encode_auth_token(client_id: str, client_shared_secret: str, request_uri: str) -> (str, str):
    request_url = re.sub(r'.*://', '', request_uri)
    nonce = str(int.from_bytes(urandom(8), byteorder))

    key = ''.join([nonce, client_shared_secret])
    token_256 = hashlib.sha256(key.encode()).digest()
    token = token_256[:16]

    timestamp = int(time.time())
    key = ''.join([nonce, request_url, str(timestamp)])
    digest_256 = hmac.new(token, msg=key.encode(), digestmod=hashlib.sha256).digest()
    digest = digest_256[:16]

    signature = base64.b64encode(digest)

    return 'hmac {0}'.format(':'.join([client_id, nonce, signature.decode('ascii')])), timestamp