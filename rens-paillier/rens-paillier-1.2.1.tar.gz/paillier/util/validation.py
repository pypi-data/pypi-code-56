from math import gcd


def validate_encryption(m, n):
    if m < 0 or m >= n:
        raise ValueError(f"m should be between 0 and {n}, was {m}")


def validate_decryption(c, n):
    upper = n**2
    if c < 0 or c >= upper:
        raise ValueError(f"c should be between 0 and {upper}, was {c}")
    if gcd(c, upper) != 1:
        raise ValueError("c and n**2 should be coprime")
