import unittest
from unittest import mock

from paillier.crypto import encrypt, decrypt, secure_addition, scalar_multiplication, secure_subtraction
from paillier.keygen import generate_keys
from paillier.util.math_shortcuts import lcm, get_mu, generate_coprime


def get_pk(case):
    return case['p'] * case['q'], case['g']


def get_sk(case):
    lam = lcm(case['p'] - 1, case['q'] - 1)
    return lam, get_mu(case['g'], lam, case['p'] * case['q'])


def get_mock(case):
    return mock.MagicMock(return_value=case['r'])


def get_msg(case):
    return case['msg']


def get_cipher(case):
    return case['cipher']


case_one = {'p': 13, 'q': 11, 'g': 19997, 'r': 6, 'msg': 47, 'cipher': 411}
case_two = {'p': 59, 'q': 53, 'g': 4023452, 'r': 553, 'msg': 1782, 'cipher': 7148516}


class TestEncryption(unittest.TestCase):

    def test_base_encryption_case_one(self):
        pk = get_pk(case_one)
        m = get_mock(case_one)
        self.assertEqual(encrypt(pk, get_msg(case_one), m), get_cipher(case_one))

    def test_basic_decryption_case_one(self):
        pk = get_pk(case_one)
        sk = get_sk(case_one)
        self.assertEqual(decrypt(pk, sk, get_cipher(case_one)), get_msg(case_one))

    def test_base_encryption_case_two(self):
        pk = get_pk(case_two)
        m = get_mock(case_two)
        self.assertEqual(encrypt(pk, get_msg(case_two), m), get_cipher(case_two))

    def test_basic_decryption_case_two(self):
        pk = get_pk(case_two)
        sk = get_sk(case_two)
        self.assertEqual(decrypt(pk, sk, get_cipher(case_two)), get_msg(case_two))


class TestHomomorphism(unittest.TestCase):
    def test_secure_addition_first(self):
        # Arrange
        pk, _ = generate_keys(k=128)
        n, _ = pk
        r = generate_coprime(n)

        e1 = encrypt(pk, 30, mock.MagicMock(return_value=r))
        e2 = encrypt(pk, 40, mock.MagicMock(return_value=r))
        expected = (e1 * e2) % n**2

        # Act
        result = secure_addition(e1, e2, n)

        # Assert
        self.assertEqual(expected, result)

    def test_secure_addition_second(self):
        # Arrange
        pk, _ = generate_keys(k=128)
        n, _ = pk
        r1, r2 = generate_coprime(n), generate_coprime(n)

        e1 = encrypt(pk, 30, mock.MagicMock(return_value=r1))
        e2 = encrypt(pk, 40, mock.MagicMock(return_value=r2))
        expected = encrypt(pk, 70, mock.MagicMock(return_value=r1*r2))

        # Act
        result = secure_addition(e1, e2, n)

        # Assert
        self.assertEqual(expected, result)

    def test_secure_addition_decryption(self):
        # Arrange
        pk, sk = generate_keys(k=128)
        n, _ = pk
        r1, r2 = generate_coprime(n), generate_coprime(n)

        e1 = encrypt(pk, 30, mock.MagicMock(return_value=r1))
        e2 = encrypt(pk, 40, mock.MagicMock(return_value=r2))

        # Act
        result = secure_addition(e1, e2, n)
        decrypted = decrypt(pk, sk, result)

        # Assert
        self.assertEqual(30 + 40, decrypted)

    def test_scalar_multiplication_first(self):
        # Arrange
        pk, _ = generate_keys(k=128)
        n, _ = pk
        c = 88

        e1 = encrypt(pk, 30)
        expected = pow(e1, c, n**2)

        # Act
        result = scalar_multiplication(e1, c, n)

        # Assert
        self.assertEqual(expected, result)

    def test_scalar_multiplication_second(self):
        # Arrange
        pk, _ = generate_keys(k=128)
        n, _ = pk
        c = 4
        r = generate_coprime(n)

        e1 = encrypt(pk, 30, mock.MagicMock(return_value=r))
        expected = encrypt(pk, 30 * c, mock.MagicMock(return_value=r**c))

        # Act
        result = scalar_multiplication(e1, c, n)

        # Assert
        self.assertEqual(expected, result)

    def test_scalar_multiplication_decryption(self):
        # Arrange
        pk, sk = generate_keys(k=12)
        n, _ = pk
        k = 4
        m = 30

        e1 = encrypt(pk, m)
        expected = (k * m) % n

        # Act
        result = scalar_multiplication(e1, k, n)
        decrypted = decrypt(pk, sk, result)

        # Assert
        self.assertEqual(expected, decrypted)

    def test_secure_subtraction_first(self):
        # Arrange
        pk, _ = generate_keys(k=128)
        n, _ = pk
        r = generate_coprime(n)
        m1 = 40
        m2 = 30

        e1 = encrypt(pk, m1, mock.MagicMock(return_value=r))
        e2 = encrypt(pk, m2, mock.MagicMock(return_value=r))
        e_minus_2 = pow(encrypt(pk, m2, mock.MagicMock(return_value=r)), n-1, n**2)
        expected = (e1 * e_minus_2) % n**2

        # Act
        result = secure_subtraction(e1, e2, n)

        # Assert
        self.assertEqual(expected, result)

    def test_secure_subtraction_decrypted(self):
        # Arrange
        pk, sk = generate_keys(k=128)
        n, _ = pk
        r = generate_coprime(n)
        m1 = 40
        m2 = 30

        e1 = encrypt(pk, m1, mock.MagicMock(return_value=r))
        e2 = encrypt(pk, m2, mock.MagicMock(return_value=r))

        # Act
        result = secure_subtraction(e1, e2, n)
        decrypted = decrypt(pk, sk, result)

        # Assert
        self.assertEqual(m1 - m2, decrypted)


if __name__ == '__main__':
    unittest.main()
