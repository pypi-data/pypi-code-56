# -*- coding: utf-8 -*-

import base64
from Crypto.Cipher import DES, AES
from Crypto import Random


def pad(s: str, block_size: int = 8):
    return s + (block_size - len(s) % block_size) * chr(block_size - len(s) % block_size)


def unpad(s):
    return s[0:-ord(s[-1])]


class DESCipher:

    def __init__(self, key):
        if len(key) < 8:
            raise ValueError("invalid key length")
        self.key = key[:8]

    def encrypt(self, raw) -> str:
        cipher = DES.new(self.key)
        msg = cipher.encrypt(pad(raw, DES.block_size))
        return base64.encodebytes(msg).decode("utf-8")

    def decrypt(self, enc: str) -> str:
        msg = base64.decodebytes(enc.encode("utf-8"))
        cipher = DES.new(self.key)
        return cipher.decrypt(msg).decode("utf-8")


class AESCipher:

    def __init__(self, key):
        self.key = key

    def encrypt(self, raw) -> str:
        raw = pad(raw, AES.block_size)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return base64.b64encode(iv + cipher.encrypt(raw)).decode("utf-8")

    def decrypt(self, enc) -> str:
        enc = base64.b64decode(enc)
        iv = enc[:16]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return unpad(cipher.decrypt(enc[16:]).decode("utf-8"))
