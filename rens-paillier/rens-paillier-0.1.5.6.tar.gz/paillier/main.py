import random
import logging
import time

from paillier.keygen import generate_keys
from paillier.crypto import encrypt, decrypt


def main():
    logging.info("Setting up key generation")
    start = time.time()
    pk, sk = generate_keys()
    n, _ = pk
    logging.info(f"Generated public and private keys, took "
                 f"{time.time() - start:.2f} seconds")
    msg = random.randrange(0, n)

    logging.info("Encrypting and decrypting message")
    logging.debug(f"{msg=}")

    before_encrypting = time.time()
    encrypted = encrypt(pk, msg)
    logging.debug(f"Encrypted message={encrypted}")
    decrypted = decrypt(pk, sk, encrypted)

    logging.info(f"Finished encrypting and decrypting msg, took "
                 f"{time.time() - before_encrypting:.2f} seconds")

    if msg == decrypted:
        logging.info("Encrypted and decrypted message with success")
    else:
        logging.error("Decrypting the original message failed. Run again with "
                      "debug logs")

    logging.info(f"Encryption and decryption took a total of "
                 f"{time.time() - start:.2f} seconds")


if __name__ == '__main__':
    main()
