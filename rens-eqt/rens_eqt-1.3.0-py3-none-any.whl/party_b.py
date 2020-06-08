from paillier.keygen import generate_keys
from paillier.crypto import decrypt, encrypt

from eqt.util.exceptions import ProtocolError
from eqt.util.log import logger


class PartyB:
    def __init__(self, k, length):
        self.x = None
        self.cis = None
        self._xis = None

        self.pk, self.sk = generate_keys(k)
        logger.debug('Generated keys, %s, %s', self.pk, self.sk)
        self._l = length

    @property
    def xis(self):
        if self._xis is None:
            x = self._decrypt_x()
            x_bits = f'{x:b}'[::-1].rjust(self._l, '0')[:self._l]
            self._xis = [encrypt(self.pk, int(x_b)) for x_b in x_bits]
        return self._xis

    def _decrypt_x(self):
        if self.x is None:
            raise ProtocolError("can't determine [xi] before [x] is given")

        return decrypt(self.pk, self.sk, self.x)

    @property
    def delta(self):
        if self.cis is None:
            raise ProtocolError("can't determine delta before cis is set")

        decrypted_cis = [decrypt(self.pk, self.sk, ci) for ci in self.cis]
        delta = 1 if any([ci == 0 for ci in decrypted_cis]) else 0
        return encrypt(self.pk, delta)
