"""
Module testcases_executor.tc_utils

Contain utils functions

Functions:
    raise_error(error_type, error_msg)
    check_type(obj, desired_classes, obj_msg)
    format_duration(duration)

Variables:
    PREFIX, MUTED, BOLD, RED, S_RESET, C_RESET: str
        colors and style
"""
PREFIX = "\x1b["
MUTED = f"{PREFIX}2m"
BOLD = f"{PREFIX}1m"
RED = f"{PREFIX}31m"
GREEN = f"{PREFIX}32m"
YELLOW = f"{PREFIX}33m"
BLUE = f"{PREFIX}36m"
MAGENTA = f"{PREFIX}35m"
S_RESET = f"{PREFIX}0m"
C_RESET = f"{PREFIX}39m"


def raise_error(error_type, error_msg):
    """
    Raise a speific type error with a formated message with info at the end.

        Parameters:
            error_type (Error): A specific type Error.
            error_msg (string): message to display.

        Raises:
            Exception (error_type): with formatted message
    """
    info_msg = "\n".join([
        f"{MUTED}\nFor more infos about usage, see README.md:",
        f"https://github.com/JBthePenguin/TestCasesExecutor{S_RESET}"])
    print(f"{BOLD}{RED}")
    raise error_type(f"{C_RESET}{error_msg}{S_RESET}\n{info_msg}\n")


def check_type(obj, desired_classes, obj_msg):
    """
    Check if an object's class is one of the desired.

        Parameters:
            obj (?): instance checked.
            desired_classes (tuple): classes checked.
            obj_msg (str): obj name used in error message.

        Raises:
            TypeError: obj not one of desired classes.
    """
    if not isinstance(obj, desired_classes):
        end_msg = " or ".join([f"'{t.__name__}'" for t in desired_classes])
        raise_error(TypeError, "".join([
            f"{obj_msg} must be {end_msg}, ",
            f"not '{obj.__class__.__name__}': {obj}"]))


def format_duration(duration):
    """
    Check if an object's class is one of the desired.

        Parameters:
            duration(time): duration in second

        Return:
            string represent duration in s if it's >1, else in ms.
    """
    if duration >= 1:
        d_unit = 's'
    else:
        duration *= 1000
        d_unit = 'ms'
    return f"{str(round(duration, 3))} {d_unit}"
