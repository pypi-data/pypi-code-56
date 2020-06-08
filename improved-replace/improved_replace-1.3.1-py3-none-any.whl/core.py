#!/usr/bin/python3


def to_array(string):
    """Converts a string to an array relative to its spaces.

    Args:
        string (str): The string to convert into array

    Returns:
        str: New array
    """

    try:
        new_array = string.split(" ")  # Convert the string into array
        while "" in new_array:  # Check if the array contains empty strings
            new_array.remove("")
        return new_array
    except:
        print("The parameter string is not a str")
        return string


def to_point(string):
    """Replaces all the commas in a string with points.

    Args:
        string (str): String to change commas for points

    Returns:
        str: String with points
    """

    # Replace the commas with points in string
    try:
        string = string.replace(",", ".")
    except:
        print("The parameter string is not a str")
    finally:
        return string


def to_comma(string):
    """Replaces all the points in a string with commas.

    Args:
        string (str): String to change points for commas

    Returns:
        str: String with commas
    """

    # Replace the points with strings in string
    try:
        string = string.replace(".", ",")
    except:
        print("The parameter string is not a str")
    finally:
        return string
