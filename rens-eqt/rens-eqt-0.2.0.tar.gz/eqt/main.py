from eqt.protocol import Protocol
from eqt.util.log import logger
from eqt.util.start import get_a_b


def main():
    a, b, l = get_a_b()
    logger.debug('a: %s, b: %s', a, b)
    p = Protocol(a, b, length=l, kappa=40)
    p.start()
    p.validate_outcome()
    print(f"Equality: {bool(p.decrypted_result)}")


if __name__ == '__main__':
    main()
