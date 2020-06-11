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

class PythonRandomContinuousIntStream :
    def __init__(self) :
        self.observed_ints = []
    
    def append_observed_bytes(self, observation) :
        self.observed_ints.extend([untemper(x) for x in observation])
    
    def is_state_fully_recovered(self) :
        return len(self.observed_ints) >= 624
    
    def get_bytestream(self, length) :
        assert self.is_state_fully_recovered()
        
        result_stream = list()
        incremental_stream = self.observed_ints.copy()
        for _ in range(length) :
            a = incremental_stream[-624]
            b = incremental_stream[-623]
            c = incremental_stream[-227]
            twisted = twist(a,b,c)
            incremental_stream.append(twisted)
            result_stream.append(temper(twisted))
        return result_stream