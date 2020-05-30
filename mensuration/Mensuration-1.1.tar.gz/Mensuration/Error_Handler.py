class ExpectedTypeError(Exception):
    # Raises the error if the Type of the args are different than expected
    def __init__(self, user_type, expected_type):
        """
        :param user_type: user entered type
        :param expected_type: the type expected
        :return : error message
        """
        self.user_type = user_type
        self.type = expected_type

    def __str__(self):
        return "Expected {} but given is {}".format(self.type, self.user_type)


class NumberOfArgumentsError(Exception):
    # Raises the error if the expected number of args are not met
    def __init__(self, given, exp_no_of_args):
        """
        :param given: Number of args the user has given
        :param exp_no_of_args: Number of args expected
        :return : error message
        """
        self.given = given
        self.exp_no_of_args = exp_no_of_args

    def __str__(self):
        return "Expected number of arguments is {} but given number of arguments is {}".format(self.exp_no_of_args,
                                                                                               self.given)


class ExpectedInputError(Exception):
    # Raises the error if the arguments passed are invalid
    def __init__(self, inputs, correct_args):
        """
        :param correct_args: valid arguments
        :param inputs: the args passed by the user
        :return : error message
        """
        self.inputs = inputs
        self.correct_args = correct_args

    def __str__(self):
        return "Expected {1} but given {0}".format(self.inputs, self.correct_args)
