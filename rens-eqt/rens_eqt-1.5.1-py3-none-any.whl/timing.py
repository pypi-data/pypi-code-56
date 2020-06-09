import time
import logging
from random import SystemRandom

from eqt.protocol import Protocol
from eqt.util.log import logger


KAPPA = 40
r = SystemRandom()


def run(length, runs, keysize):
    logger.info('Performing %s runs with length %s', runs, length)

    start = time.time()
    for _ in range(runs):
        a, b = r.getrandbits(length), r.getrandbits(length)
        p = Protocol(a, b, KAPPA, keysize)
        p.start()
        p.validate_outcome()

    elapsed_time = (time.time() - start) * 1000
    logger.info(f'Performed %s runs with length %s. Average time: {elapsed_time / runs:.4}ms',
                runs, length)


def timing(runs=100, keysize=2048):
    logger.setLevel(level=logging.INFO)
    run(10, runs, keysize)
    run(20, runs, keysize)
    run(50, runs, keysize)
    run(100, runs, keysize)


if __name__ == '__main__':
    timing()
