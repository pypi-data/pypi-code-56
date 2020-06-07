from random import getrandbits, shuffle

from paillier.crypto import encrypt, secure_addition, scalar_multiplication, secure_subtraction

from eqt.util.exceptions import ProtocolError
from eqt.util.log import logger


class PartyA:
    def __init__(self, pk, a, b, length, kappa):
        self.xis, self.xors, self.cis, self.delta_b = None, None, None, None

        self._pk = pk
        self._n, _ = pk
        self._a = a
        self._b = b
        self._l = length
        self._k = kappa

        self._r = None
        self._delta = None

    def generate_r(self):
        self._r = getrandbits((self._l + 1 + self._k) // 2)
        logger.debug('r: %s', self._r)

    @property
    def x(self):
        try:
            return secure_addition(secure_subtraction(self._a, self._b, self._n),
                                   encrypt(self._pk, self._r), self._n)
        except TypeError:
            raise ProtocolError("x was accessed before r was generated.")

    def compute_xor(self):
        if self.xis is None:
            raise ProtocolError("xis was accessed before it was set")

        r_bits = f'{self._r:b}'[::-1].rjust(len(self.xis), '0')[:len(self.xis)]
        assert len(r_bits) == len(self.xis), f"r_bits and xis should be the same length, are " \
                                             f"{len(r_bits)} and {len(self.xis)}"

        self.xors = list(self._get_xor(r_bits, self.xis))

    def determine_delta(self):
        # self._delta = randrange(0, 2)
        self._delta = 1

    def compute_cis(self):
        if self._delta == 0:
            self._compute_cis_hamming()
        else:
            self._compute_cis_comparison()
        pass

    def _compute_cis_hamming(self):
        c0 = self._compute_c0()
        logger.debug('[c0]: %s', c0)
        cis = [encrypt(self._pk, getrandbits(self._k // 2))
               for _ in range(self._l - 1)]
        self.cis = [c0] + cis

    def _compute_c0(self):
        c0 = self._product(self.xors)
        p = getrandbits(self._k)
        return scalar_multiplication(c0, p, self._n)

    def _compute_cis_comparison(self):
        cis = list(self._build_cis_comparison())
        self.cis = [scalar_multiplication(ci, getrandbits(self._k), self._n) for ci in cis]

    def _build_cis_comparison(self):
        total_prod = self._product(self.xors)
        for i in range(0, self._l):
            neg_1 = encrypt(self._pk, -1)

            if i == self._l - 1:
                prod_square = encrypt(self._pk, 0)
            else:
                prod = self._product(self.xors, i+1)
                prod_square = scalar_multiplication(prod, 2, self._n)

            result = secure_addition(total_prod, prod_square, self._n)
            result = secure_addition(neg_1, result, self._n)
            yield result

    def shuffle_cis(self):
        if self.cis is None:
            raise ProtocolError("[ci] was shuffled before it was set")
        shuffle(self.cis)

    @property
    def curly_theta(self):
        if self._delta == 0:
            return self.delta_b
        return self._inverse(self.delta_b)

    def _get_xor(self, r_bits, x_bits):
        for ri, xi in zip(r_bits, x_bits):
            if int(ri) == 0:
                yield int(xi)
            else:
                yield self._inverse(xi)

    def _product(self, xors, start=0):
        r = xors[start]
        for x in xors[start+1:]:
            r = secure_addition(r, x, self._n)
        return r

    def _inverse(self, ciphertext):
        inverse_xi = scalar_multiplication(ciphertext, -1, self._n)
        e1 = encrypt(self._pk, 1)
        return secure_addition(inverse_xi, e1, self._n)
