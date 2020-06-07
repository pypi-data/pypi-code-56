import unittest
from models.RomanInteger import RomanInteger

class TestRomanInteger(unittest.TestCase):
    def test_roman_integer_to_integer(self):
        roman = 'XI'
        integer = 11

        result = RomanInteger(roman).to_integer()

        self.assertTrue(result == integer)
