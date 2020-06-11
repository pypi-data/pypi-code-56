import unittest
from ..context import cryptraider



class TestContinuousIntStream(unittest.TestCase):
    def test_base_case(self):
        # Find the solutions to the equation x^2 = 1 (mod 2^2)
        roots = cryptraider.math.find_square_roots_mod_2power(1, 2)
        self.assertListEqual([1, 3], roots)

        
        # Find the solutions to the equation x^2 = 1 (mod 2^2)
        roots = cryptraider.math.find_square_roots_mod_2power(3, 2)
        self.assertListEqual([], roots)

    
    def test_all_equations_mod_256(self):
        correctAnswers = dict([ (i, list()) for i in range(256) ])
        for i in range(256) :
            correctAnswers[i**2 % 256].append(i)
        
        # Find the solutions to the equation x^2 = 1 (mod 2^2)
        for i in range(256) :
            roots = cryptraider.math.find_square_roots_mod_2power(i, 8)
            self.assertListEqual(correctAnswers[i], roots, "test case failed for i=%d"%i)