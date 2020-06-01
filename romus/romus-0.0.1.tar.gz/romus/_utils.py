"""
"""

import logging as logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

################################################################################

def check_fitted(f):
    """
    """
    def wrapper(*args, **kwargs):
        self = args[0]
        if self.fitted is False:
            raise Exception("Please fit model before using posterior methods.")
        return f(*args, **kwargs)
    return wrapper

################################################################################

def check_input_gt_zero(input, input_name):
    """
    Check that the input is greater than zero.
    """
    if input is not None and input <= 0:
        raise ValueError("Input {} must be greater than 0.".format(input_name))

def check_input_state(input, attribute, input_name):
    """
    Handle cases where the attribute already exists or does not exits.
    """

    if input is None and attribute is None:
        raise ValueError("Must specify value for {}.".format(input_name))

    if input is not None:
        if attribute is not None:
            logger.warning("Overriding previous value of {} with input to "
            "fit() method.".format(input_name))
        return input

    return attribute
