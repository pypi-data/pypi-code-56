# Importing required modules
from Mensuration.Parameters import Parameters, uninitialized_params_check
from Mensuration.Error_Handler import *


class Area(Parameters):

    def __init__(self, radius=None, length=None, base=None, height=None, width=None):

        # Initializing the Area_parameters
        Parameters.__init__(self, radius, length, base, height, width)

    def Square(self):  # edge_length^2
        edge_length = self.length
        return edge_length * edge_length

    def Circle(self):  # π × radius^2
        return self.pi * self.radius ** 2

    def Triangle(self):  # 1/2 * base  * height
        return self.base * self.height * 0.5

    def Rectangle(self):  # length * width
        return self.length * self.width

    def Parallelogram(self):  # base * height
        return self.base * self.height

    def Trapezium(self, length_of_parallel_sides):  # 0.5 * (a+b) × h

        sum = 0

        len_of_inputs = len(length_of_parallel_sides)
        expectedArgs = 2  # Expected number of args

        """To check whether the number of inputs are
                in the expected range"""

        if len_of_inputs != expectedArgs:
            raise NumberOfArgumentsError(len_of_inputs, expectedArgs)
        else:
            for x in length_of_parallel_sides:
                sum += x
            return 0.5 * sum * self.height

    def Ellipse(self, minor_axis, major_axis):  # π * a * b
        expected_type_order = [[int, float], [int, float]]
        result, user_type_order = uninitialized_params_check(expected_type_order, [minor_axis, major_axis])

        if result:
            return self.pi * minor_axis * major_axis
        else:
            raise ExpectedTypeError(user_type_order, "[<class 'int'>] or [<class 'float'>]")

