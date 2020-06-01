import random
import logging
logging.basicConfig(format='%(message)s', level=logging.INFO)

class Generation:
    """Generic generation class for random numbers"""

    def __init__(self, n):

        """ Args:
            number(int)

        Attributes:
            n(int) representing the number of guessed numbers
        """

        logging.info('Welcome to your Number Game')
        self.n = int(n)
