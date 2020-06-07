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
        p = Protocol(a, b, length, KAPPA)
        p.start()
        # p.validate_outcome()

    elapsed_time = time.time() - start
    logger.info(f'Performed %s runs with length %s. Average time: {elapsed_time / runs:.2}s',
                runs, length)


def main():
    logger.setLevel(level=logging.INFO)
    run(10)
    run(20)
    run(50)
    run(100)


if __name__ == '__main__':
    main()
