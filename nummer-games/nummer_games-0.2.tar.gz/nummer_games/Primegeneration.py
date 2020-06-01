from .Genericgeneration import Generation
import logging


class Prime(Generation):
    """ Prime class for classifying prime number from guesses.

    Attributes:
		n(integer) - number of attempts
	"""
    def __init__(self, n):
        super().__init__(n)

    def guess_prime_number(self):
        """Function to read in number entered by user in n attempts.
           Check for factors, if the remainder beween the modulus division of
           the divisor and the input is equal to zero then it is not a
           prime number otherwise it is a prime number. If Input number is less
           than or equal to 1 then it is not prime

		Args:
			guess(integer): the user entered number

		Returns:
			string: What a Prime number is and characteristics of not a Prime number
		"""
        attempts = 0
        while attempts < self.n:
            # Enter a number
            item = int(input("Write a number:"))
            if item > 1:
                # check for factors
                for i in range(2, item):
                    if (item % i) == 0:
                        logging.info(f" {item},is not a prime number")
                        logging.info(f" {i} multiplied by, {item//i} is {item}")
                        break
                else:
                    logging.info(f" {item}, is a prime number")
            else:
                logging.info(f" {item}, is not a prime number")

            attempts += 1
        if attempts == self.n:
            logging.info(f"END!!! {attempts} attempts succesfully made")
