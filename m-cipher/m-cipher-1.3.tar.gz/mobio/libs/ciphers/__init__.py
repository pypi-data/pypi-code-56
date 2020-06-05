import base64
import hashlib

import numpy as np


class MobioCrypt2:
    @staticmethod
    def __f1(x1):
        x = v = 1
        y = u = 0
        a = 0x100
        b = x1 % 0x100
        while b != 0:
            q = int(a / b)
            r = int(a - b * q)
            s = int(x - u * q)
            t = int(y - v * q)
            a = b
            x = u
            y = v
            b = r
            u = s
            v = t
        while y < 0:
            y += 0x100
        while y > 0x100:
            y -= 0x100
        return y

    @staticmethod
    def __f2():
        return np.random.randint(1, 0x100, 0x0A)

    @staticmethod
    def e1(raw):
        if isinstance(raw, str):
            raw = raw.encode('utf-8')

        ln = len(raw)

        r1 = bytearray()
        tmp = MobioCrypt2.__f2()

        for i in range(0, len(tmp)):
            r1.append(tmp[i])

        i = r1[0]
        k = r1[1]

        i += 1 if i % 2 == 0 else 0
        i = 0x8F if i == 1 else i

        for j in range(0, ln):
            tmp = (int(raw[j]) * i + k + r1[(2 + (j % 8))]) % 0x100
            while tmp >= 0x100:
                tmp -= 0x100
            while tmp < 0:
                tmp += 0x100
            r1.append(tmp)
        r1 = MobioCrypt3.e1(r1).rstrip('=')
        return r1 + hashlib.md5(r1.encode('utf-8')).hexdigest()

    @staticmethod
    def d1(encrypted, enc=None):
        raw = encrypted[0:len(encrypted)-0x20]
        c1 = encrypted[len(encrypted)-0x20:]
        c2 = hashlib.md5(raw.encode('utf-8')).hexdigest()
        if c2 != c1:
            return None

        raw = MobioCrypt3.d1(raw)
        ln = len(raw)

        i = raw[0]
        i += 1 if i % 2 == 0 else 0
        i = 0x8F if i == 1 else i

        lc = MobioCrypt2.__f1(i)
        m = raw[1]
        r1 = bytearray()
        for j in range(10, ln):
            tmp = ((int(raw[j]) - raw[(2 + ((j-int(0x0A)) % 8))] - m) * lc) % 0x100
            while tmp >= 0x100:
                tmp -= 0x100
            while tmp < 0:
                tmp += 0x100
            if j >= 10:
                r1.append(tmp)
        if enc:
            return r1.decode(encoding=enc)
        return r1


class MobioCrypt3:
    @staticmethod
    def e1(raw):
        try:
            bs = raw
            if isinstance(raw, str):
                bs = raw.encode('utf-8')

            ed = base64.b64encode(bs)
            return ed.decode(encoding='UTF-8')
        except:
            return ""

    @staticmethod
    def e2(raw):
        return MobioCrypt3.e1(raw).rstrip('=')

    @staticmethod
    def d1(raw, enc=None):
        try:
            if isinstance(raw, bytes):
                raw = raw.decode('UTF-8')
            dd = base64.urlsafe_b64decode(raw + '=' * (-len(raw) % 4))
            if enc:
                return dd.decode(encoding=enc)
            return dd
        except:
            return None