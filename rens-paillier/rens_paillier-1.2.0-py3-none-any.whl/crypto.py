import logging

from paillier.util.math_shortcuts import generate_coprime, l_x
from paillier.util.validation import validate_encryption, validate_decryption


def encrypt(pk, plaintext, r_generate=generate_coprime):
    n, g = pk
    plaintext = plaintext % n
    validate_encryption(plaintext, n)

    r = r_generate(n)
    logging.debug(f"{r=}")
    return pow(g, plaintext, n ** 2) * pow(r, n, n ** 2) % n ** 2


def decrypt(pk, sk, ciphertext):
    n, _ = pk
    validate_decryption(ciphertext, n)
    lam, mu = sk
    logging.debug(f"{n=}, {lam=}, {mu=}")

    x = pow(ciphertext, lam, n**2)
    lx = l_x(x, n)
    logging.debug(f"{x=}, l(x)={lx}")
    return (lx * mu) % n


def secure_addition(ciph1, ciph2, n):
    return (ciph1 * ciph2) % n**2


def scalar_multiplication(ciphertext, k, n):
    return pow(ciphertext, k, n ** 2)


def secure_subtraction(ciph1, ciph2, n):
    n_sq = n**2
    minus_ciph2 = pow(ciph2, n-1, n_sq)
    return (ciph1 * minus_ciph2) % n_sq
