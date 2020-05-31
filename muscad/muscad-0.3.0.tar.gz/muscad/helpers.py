import math
import re

pi = math.pi
radians = math.radians
degrees = math.degrees


def normalize_angle(angle):
    """
    Normalize an angle value in degrees.
    :param angle: an angle value, in degrees
    :return: an angle between 0 included and 360 excluded
    """
    while angle < 0:
        angle = angle + 360
    while angle >= 360:
        angle = angle - 360
    return angle


def cos(deg: float):
    """
    Returns the cosinus of angle in degrees
    :param deg: an angle, in degrees
    :return: a cosine, between 0 and 1
    """
    return math.cos(math.radians(deg))


def sin(deg: float):
    """
    Returns the sinus of an angle in degrees
    :param deg: an angle, in degrees
    :return: a sine, between 0 and 1
    """
    return math.sin(math.radians(deg))


def tan(deg: float):
    """
    Returns the arc tangent of an angle in degrees
    :param deg: an angle, in degrees
    :return: an arc tangent
    """
    return math.tan(math.radians(deg))


def acos(x: float):
    """
    Returns the arc cosine of x, in degrees
    :param x: a float
    :return: the arc cosine in degrees
    """
    return math.degrees(math.acos(x))


def asin(x: float):
    """
    Returns the arc sine of x, in degrees
    :param x: a float
    :return: the arc sine in degrees
    """
    return math.degrees(math.asin(x))


def atan(x: float):
    """
    Returns the arc tangeant of x, in degrees
    :param x: a float
    :return: the arc tangent in degrees
    """
    return math.degrees(math.atan(x))


def atan2(x: float, y: float):
    return math.degrees(math.atan2(x, y))


def hypotenuse(leg1, leg2):
    """
    Returns the length of the hypotenuse based on the length of both legs
    :param leg1: length of one leg
    :param leg2: length of the other leg
    :return: the hypotenuse length
    """
    return (leg1 ** 2 + leg2 ** 2) ** 0.5


def catheti(hypot, leg):
    """
    Returns the length of one leg based on the length of the hypotenuse and the other leg
    :param hypot: length of the hypotenuse
    :param leg: length of the other leg
    :return: the length of the missing leg
    """
    return (hypot ** 2 - leg ** 2) ** 0.5


def camel_to_snake(name):
    """
    Transform a CamelCase name (like Python class names) into
    a snake_case name (like OpenSCAD object names).
    :param name: a name in CamelCase
    :return: a name in snake_case
    """
    name = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", name)
    return re.sub("([a-z0-9])([A-Z])", r"\1_\2", name).lower()
