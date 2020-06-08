import time
import logging
from random import getrandbits

from eqt.protocol import Protocol
from eqt.util.log import logger


KAPPA = 40


def run(length, runs=100):
    logger.info('Performing %s runs with length %s', runs, length)

    start = time.time()
    for _ in range(100):
        a, b = getrandbits(length), getrandbits(length)
        p = Protocol(a, b, KAPPA)
        p.start()
        p.validate_outcome()

    elapsed_time = (time.time() - start) * 1000
    logger.info(f'Performed %s runs with length %s. Average time: {elapsed_time / runs:.4}ms',
                runs, length)


def timing():
    logger.setLevel(level=logging.INFO)
    run(10)
    run(20)
    run(50)
    run(100)


if __name__ == '__main__':
    timing()
