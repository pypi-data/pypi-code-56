#!/usr/bin/python3
class ImprovedReplace:
    """Class to improve replace method

    Class to add some replace method improvements focused on
    common replacements to optimize code.
    """

    @classmethod
    def to_array(cls, string):
        """Converts a string to an array relative to its spaces."""

        new_array = string.split(" ")  # Convert the string into array
        while "" in new_array:  # Check if the array contains empty strings
            new_array.remove("")

        return new_array

    @classmethod
    def comma_to_point(cls, string):
        """Replaces all the commas in a string with points."""

        string = string.replace(",", ".")  # Replace the commas with points in string
        return string

    @classmethod
    def point_to_comma(cls, string):
        """Replaces all the points in a string with commas."""

        string = string.replace(".", ",")  # Replace the points with commas in string
        return string
