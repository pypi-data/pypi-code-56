import unittest

from paillier.util.math_shortcuts import l_x, lcm, get_mu


class TestKeyGen(unittest.TestCase):
    def test_lx(self):
        self.assertEqual(l_x(127, 21), 6)
        self.assertEqual(l_x(736, 21), 35)
        self.assertEqual(l_x(496, 33), 15)

    def test_lcm(self):
        self.assertEqual(lcm(46757-1, 29755-1), 695589012)
        self.assertEqual(lcm(7-1, 5-1), 12)
        self.assertEqual(lcm(5-1, 7-1), 12)

    def test_mu(self):
        self.assertEqual(get_mu(36, 12, 35), 3)
        self.assertEqual(get_mu(907, 10, 33), 28)


if __name__ == '__main__':
    unittest.main()
