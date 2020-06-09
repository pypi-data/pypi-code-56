import unittest

from paillier.util.prime_test import naive_test


class MyTestCase(unittest.TestCase):
    def test_naive_test(self):
        self.assertEqual(naive_test(215), False)
        self.assertEqual(naive_test(26), False)
        self.assertEqual(naive_test(248), False)
        self.assertEqual(naive_test(31), True)
        self.assertEqual(naive_test(216), False)


if __name__ == '__main__':
    unittest.main()
