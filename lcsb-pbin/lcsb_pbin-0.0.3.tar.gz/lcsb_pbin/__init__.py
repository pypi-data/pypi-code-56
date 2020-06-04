#!/usr/bin/env python

import requests
import zlib
import json

from requests.auth import HTTPBasicAuth
from base64 import b64encode, b64decode
from hashlib import sha256
from sjcl import SJCL
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes


FORMATTER = ("plaintext", "syntaxhighlighting", "markdown")
EXPIRE = ("5min", "10min", "1hour", "1day", "1week", "1month")


def json_encode(s):
    return json.dumps(s, separators=(",", ":")).encode()


def compress(text):
    co = zlib.compressobj(wbits=-zlib.MAX_WBITS)
    b = co.compress(text) + co.flush()
    return b64encode("".join(map(chr, b)).encode("utf-8"))


def preparePassKey(key, password):
    if password is not None:
        digest = sha256(password.encode("UTF-8")).hexdigest()
        return b64encode(key) + digest.encode("UTF-8")
    return b64encode(key)


def encrypt(
    text,
    password=None,
    burnafterreading=0,
    expire="1day",
    formatter="plaintext",
    opendiscussion=0,
):
    key = get_random_bytes(32)
    data = {
        "expire": expire,
        "formatter": formatter,
        "burnafterreading": int(burnafterreading),
        "opendiscussion": int(opendiscussion),
    }
    passKey = preparePassKey(key, password)
    cipher = SJCL().encrypt(
        compress(text.encode("utf-8")), passKey, mode="gcm", dkLen=32
    )
    for k in ["salt", "iv", "ct"]:
        cipher[k] = cipher[k].decode()
    data["data"] = json_encode(cipher)
    return b64encode(key).decode(), data


def paste(
    server,
    text,
    username,
    password,
    paste_password=None,
    formatter="plaintext",
    opendiscussion=False,
    burnafterreading=False,
    expire="1day",
    debug=False,
):
    """
    Send a Paste to the LCSB - privatebin.
    Only people with correct credentials can actually paste data as it is protected
    with basic auth.
    server: address of the privatebin server: https://privatebin.lcsb.uni.lu/
    text: the paste data
    username: username for basic auth
    password: password for basic auth
    paste_password: put password to protect paste - default: None
    formatter: paster format to use: plaintext, syntaxhighlighting, markdown - default: plaintext
    opendiscussion: if you want to allow comments - default: False
    burnafterreading: burn the paste after it has been seen once - default False
    expire: paste expiration time, it can be 5min, 10min, 1hour, 1day, 1week, 1month - default 1day
    debug:" print response status code - default False
    return: the privatebin link
    """
    if formatter not in FORMATTER:
        raise KeyError(f"'formatter' should be one of: {', '.join(FORMATTER)}")
    if expire not in EXPIRE:
        raise KeyError(f"'expire' should be one of: {', '.join(EXPIRE)}")
    key, data = encrypt(
        text, paste_password, burnafterreading, expire, formatter, opendiscussion
    )
    if debug:
        print(f"Request data:\t{data}")
    response = requests.post(
        server,
        data=data,
        auth=HTTPBasicAuth(username, password),
        headers={"X-Requested-With": "JSONHttpRequest"},
    )
    if debug:
        print(f"Status code:\t{response.status_code}")
        print(f"Response:\t{response}")
        print(f"Key:\t{key}")
    if response.status_code != 200:
        raise RuntimeError(
            f"No paste can be generated: {response.status_code} - {response.content}"
        )
    result = response.json()
    if debug:
        print(f"Result: {result}")
    return f"{server}?{result['id']}#{key}"
