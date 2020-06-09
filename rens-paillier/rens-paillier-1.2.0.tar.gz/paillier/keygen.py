import time
import logging

from paillier.util.math_shortcuts import generate_coprime, lcm, get_mu
from paillier.util.prime_generation import miller_rabin_generation as generate_prime


def generate_keys(k=2048):
    k = KeyGen(k)
    pk = PublicKey(k.pk)
    sk = SecretKey(k.sk)
    return pk, sk


class KeyGen:
    def __init__(self, k=2048):
        self._setup(k)

    def _setup(self, k):
        self._k = k
        self._p, self._q = self._get_p_q(self._k)

        self._lam = lcm(self._p - 1, self._q - 1)
        self._n = self._p * self._q
        self._g = generate_coprime(self._n ** 2)
        self._mu = get_mu(self._g, self._lam, self._n)

        self._log_variables()

    def _log_variables(self):
        logging.debug(f"{self._k=}, {self._p=}, {self._q=}, {self._n=}, "
                      f"{self._lam=}, {self._mu=}, {self._g=}")

    @property
    def pk(self):
        return self._n, self._g

    @property
    def sk(self):
        return self._lam, self._mu

    @staticmethod
    def _get_p_q(k):
        length = int(k // 2)
        start = time.time()
        p, q = generate_prime(length), generate_prime(length)
        while p == q:
            q = generate_prime(length)
        logging.debug(f"Generating primes took "
                      f"{time.time() - start:.2f} seconds")
        return p, q

    def __str__(self):
        return f"{self.pk}"

    def __repr__(self):
        return f"<KeyGen: {self.pk=}, {self.sk=}>"


class PublicKey:
    def __init__(self, pk):
        self.n, self.g = pk

    def __str__(self):
        return f"pk = ({self.n}, {self.g})"

    def __repr__(self):
        return f"<PublicKey: {self.n=}, {self.g=}>"

    def __iter__(self):
        return iter((self.n, self.g))

    def __getitem__(self, item):
        return list(self)[item]


class SecretKey:
    def __init__(self, sk):
        self.lam, self.mu = sk
        self._validate_sk()

    def _validate_sk(self):
        if self.lam is None or self.mu is None:
            raise ValueError("Secret key was not properly set up")

    def __str__(self):
        return f"sk = ({self.lam}, {self.mu})"

    def __repr__(self):
        return f"<PrivateKey: {self.lam=}, {self.mu=}>"

    def __iter__(self):
        return iter((self.lam, self.mu))
