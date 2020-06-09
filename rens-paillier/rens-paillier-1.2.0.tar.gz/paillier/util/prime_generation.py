from random import SystemRandom

from paillier.util.prime_test import naive_test, miller_rabin_test


r = SystemRandom()


def naive_generation(q):
    # O(sqrt(n))
    n = r.getrandbits(q)
    while not (naive_test(n) and n > 2):
        n = r.getrandbits(q)
    return n


def generate_prime_candidate(length):
    p = r.getrandbits(length)
    # apply a mask to set MSB and LSB to 1
    p |= (1 << length - 1) | 1

    return p


def miller_rabin_generation(length=1024):
    p = 4
    # keep generating while the primality test fail
    while not miller_rabin_test(p, 128):
        p = generate_prime_candidate(length)
    return p
