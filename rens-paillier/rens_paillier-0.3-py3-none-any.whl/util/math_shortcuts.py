import random
from math import gcd
from functools import lru_cache


@lru_cache
def l_x(x, n):
    return int((x-1) // n)


@lru_cache
def lcm(p, q):
    return p * q // gcd(p, q)


@lru_cache
def get_mu(g, lam, n):
    return pow(
        l_x(
            pow(g, lam, n**2), n),
        -1,
        mod=n)


def generate_coprime(upper):
    n = random.randrange(0, upper)
    while gcd(n, upper) != 1:
        n = random.randrange(0, upper)
    return n