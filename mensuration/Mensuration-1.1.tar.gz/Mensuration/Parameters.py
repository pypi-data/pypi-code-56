from Mensuration.Error_Handler import *
import math


def uninitialized_params_check(type_expected_list, params):
    """
    Parameters that are not initialized during instantiation,
    but during a call of a function.

    The goal is to check weather the parameters are of correct
    type
    :param type_expected_list: the list of expected args type
    :param params: user defined parameters
    :return: (True,None) or (False, params_type_copy)
    """
    ''' converting the inputs to its type. This will be changed accordingly if
         there's a list in type_expected parameters'''
    params_type = [type(x) for x in params]

    params_type_copy = params_type.copy()  # making a copy of the original params_type without any change to return
    type_expected_list_new = []  # this new variable contains the list inside type_expected_list if there's any
    params_type_new = []  # this new variable contains the corresponding params_type to type_expected_list_new
    bool_list = []  # contains bool values

    for i, x in enumerate(type_expected_list):
        """
           If the type_expected_list contains a list inside,
           the code below appends True if params_type[i] in 
           the list or else appends False 
        """

        # print(len(type_expected_list_copy))
        if type(x) is list:
            type_expected_list_new.append(type_expected_list[i])
            params_type_new.append(params_type[i])
            if params_type[i] in x:
                bool_list.append(True)
            else:
                bool_list.append(False)
        else:
            pass
    # print(type_expected_list)

    [type_expected_list.remove(x) for x in type_expected_list_new]
    [params_type.remove(x) for x in params_type_new]
    # print(type_expected_list)

    # print(params_type)
    # print(bool_list)
    if params_type == type_expected_list and False not in bool_list:
        return True, None
    else:

        return False, params_type_copy


# print(uninitialized_params_check([[float, int], [float, int], [str, int]], [5.05, 'str', 5]))


class Parameters:

    def __init__(self, radius, length, base, height, width):

        # CODE for if parameters are **kwargs (incomplete & dropped)

        """self.measurements = []
        self.values = []

        # m = measurements['radius','length',...]
        #v = values

        possible_measurements = ['radius','length','base','height','width']# these measurements are allowed
        
        # separating the arguments and values passed
        for m,v in measurements_values.items():
            
            if m in possible_measurements:
                setattr(self,m,v) #making the arguments an instance
                self.measurements.append(m)
                self.values.append(v)
            .
            .
            .

            """

        self.radius = radius
        self.height = height
        self.width = width
        self.length = length
        self.base = base
        self.pi = math.pi

        list_of_measurements = [self.radius, self.height, self.width, self.length, self.base]

        # Checking if the inputs are other than integer value
        for m in list_of_measurements:
            if type(m) == int or m is None:
                pass
            else:
                integer = int
                m = type(m)
                raise ExpectedTypeError(m, integer)

    def to_radians(self, theta):
        degree = theta
        return degree * self.pi / 180

    def to_degrees(self, theta):
        radians = theta
        int_value = []
        pi = []
        """ Iterating over the string to get 
            the integer part out"""

        for word in radians.split('_'):
            if word.isdigit():
                int_value.append(int(word))
            else:
                pi.append(word)
        try:
            if 'pi' in pi:
                return int_value[0] * self.pi * 180 / self.pi
            else:
                raise ExpectedInputError(radians, 'value_pi')
        except:
            raise ExpectedInputError(radians, 'value_pi')
