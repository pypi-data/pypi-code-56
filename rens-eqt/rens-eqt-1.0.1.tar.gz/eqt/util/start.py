from eqt.util.exceptions import ProtocolError
from eqt.util.log import logger


def get_a_b():
    def get_inputs():
        a = int(input("Input value a: "))
        b = int(input("Input value b: "))

        return a, b

    def get_hardcoded():
        a, b = 12313, 12312
        import random
        if random.randrange(0, 2) == 1 and False:
            b = a

        logger.info('a b equal: %s', a == b)
        return a, b

    return get_hardcoded()
