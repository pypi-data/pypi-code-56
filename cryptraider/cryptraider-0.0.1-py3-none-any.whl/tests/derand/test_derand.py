import unittest
from ..context import cryptraider

import random

class TestContinuousIntStream(unittest.TestCase):
    def test_default_state(self):
        derand = cryptraider.derand.PythonRandomContinuousIntStream()
        self.assertFalse(derand.is_state_fully_recovered())
        
    def test_not_enough_observations(self):
        derand = cryptraider.derand.PythonRandomContinuousIntStream()
        derand.append_observed_bytes([0 for _ in range(623)])
        self.assertFalse(derand.is_state_fully_recovered())

        derand.append_observed_bytes([0])
        self.assertTrue(derand.is_state_fully_recovered())
 
    def test_simple_bytestream(self):
        N = 1000
        chunk1 = [random.getrandbits(32) for i in range(N)]
        chunk2 = [random.getrandbits(32) for i in range(N)]

        derand = cryptraider.derand.PythonRandomContinuousIntStream()
        
        
        self.assertFalse(derand.is_state_fully_recovered())
        derand.append_observed_bytes(chunk1)

        self.assertTrue(derand.is_state_fully_recovered())
        calculated_bytes = derand.get_bytestream(len(chunk2))
        self.assertEqual(chunk2, calculated_bytes)
    
    def test_larger_bytestream(self):
        chunk1 = [random.getrandbits(32) for i in range(624)]
        chunk2 = [random.getrandbits(32) for i in range(10000)]

        derand = cryptraider.derand.PythonRandomContinuousIntStream()
        derand.append_observed_bytes(chunk1)

        self.assertTrue(derand.is_state_fully_recovered())
        calculated_bytes = derand.get_bytestream(len(chunk2))
        self.assertEqual(chunk2, calculated_bytes)

def temper(x):
    x ^= x >> 11
    x ^= (x << 7) & 0x9d2c5680
    x ^= (x << 15) & 0xefc60000
    x ^= x >> 18
    return (x & 0xffffffff)

def unshiftLeft(x, shift, mask):
    res = x
    for _ in range(32):
        res = x ^ (res << shift & mask)
    return res

def unshiftRight(x, shift):
    res = x
    for _ in range(32):
        res = x ^ res >> shift
    return res

def untemper(x):
    x = unshiftRight(x, 18)
    x = unshiftLeft(x, 15, 0xefc60000)
    x = unshiftLeft(x, 7, 0x9d2c5680)
    x = unshiftRight(x, 11)
    return x

def twist(a, b, c) :
    x = ((a & 0x80000000) + (b & 0x7fffffff)) & 0xFFFFFFFF
    twisted = c ^ (x >> 1)

    if x & 1 != 0:
        twisted ^= 0x9908b0df
    return twisted

class PythonRandRangeStream :
    """This class can be used to extract the internal state based on an integer stream generated using 
    python's random.randrange(upperBoundExclusive). 

    This algorithm is not meant to be super efficient or work with as few bytes as possible, it could certainly 
    be improved.
    """
    def __init__(self, upperBoundExclusive=None) :
        self.observed_ints = []
        self.upperBoundExclusive = upperBoundExclusive
    
    def append_observed_bytes(self, observation) :
        self.observed_ints.extend([untemper(x) for x in observation])
    
    def is_state_fully_recovered(self) :
        return self.attempt_state_recovery()
    
    def attempt_state_recovery(self) :
        arr = self.observed_ints
        # First pass, we want to find all matches that are visible
        # a = 0
        # b = 1
        # c = 397
        # d = 624
        if len(self.observed_ints) < 1000 : # Arbitrary number - you could do a lot with less than 1000 bytes
            return False
        
        matches = list()
        for a in range(len(arr)) :
            b = a+1
            found = False
            for c in range(a+300, 398) :
                for d in range(c+128, 625) :
                    if twist(arr[a], arr[b], arr[c]) == arr[d] :
                        matches.append(a,b,c,d)
                        found = True
                        break
                if found :
                    break
        print('Matches found: ',len(matches))
        return False

    def get_bytestream(self, length) :
        assert self.is_state_fully_recovered()
        
        result_stream = list()
        incremental_stream = self.observed_ints.copy()
        for _ in range(length) :
            a = incremental_stream[-624]
            b = incremental_stream[-623]
            c = incremental_stream[-227]

            x = ((a & 0x80000000) + (b & 0x7fffffff)) & 0xFFFFFFFF
            twisted = c ^ (x >> 1)

            if x & 1 != 0:
                twisted ^= 0x9908b0df
            incremental_stream.append(twisted)
            result_stream.append(temper(twisted))
        return result_stream

class TestRandRangeStream(unittest.TestCase):
    def test_default_state(self):
        derand = cryptraider.derand.PythonRandomContinuousIntStream()
        self.assertFalse(derand.is_state_fully_recovered())
        
    def test_derand (self):
        derand = cryptraider.derand.PythonRandomContinuousIntStream()
        derand.append_observed_bytes([0 for _ in range(623)])
        self.assertFalse(derand.is_state_fully_recovered())

        derand.append_observed_bytes([0])
        self.assertTrue(derand.is_state_fully_recovered())
 
if __name__ == '__main__':
    unittest.main()