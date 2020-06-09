#!/usr/bin/env python
"""Bashcalc: Evaluating math expression from terminal in terminal."""
import argparse
from decimal import Decimal, InvalidOperation
from math import *
import sys

from . import __version__


class ColorFont:
    """Color and Fontsstyle Attributes for printing."""

    resetall = "\033[0m"
    # Colors
    default = "\033[39m"
    black = "\033[30m"
    red = "\033[31m"
    green = "\033[32m"
    yellow = "\033[33m"
    blue = "\033[34m"
    magenta = "\033[35m"
    cyan = "\033[36m"
    lightgray = "\033[37m"
    darkgray = "\033[90m"
    lightred = "\033[91m"
    lightgreen = "\033[92m"
    lightyellow = "\033[93m"
    lightblue = "\033[94m"
    lightmagenta = "\033[95m"
    lightcyan = "\033[96m"
    white = "\033[97m"
    # Fontstyle
    bold = "\033[1m"
    dim = "\033[2m"
    italic = "\033[3m"
    underlined = "\033[4m"
    blink = "\033[5m"
    reverse = "\033[7m"
    hidden = "\033[8m"
    # Fontstyle reset
    resetbold = "\033[21m"
    resetdim = "\033[22m"
    resetitalic = "\033[23m"
    resetunderlined = "\033[24m"
    resetblink = "\033[25m"
    resetreverse = "\033[27m"
    resethidden = "\033[28m"


def log_message(msg, mode=None):
    """Print messages to display.
    
    Parameters
    ----------
    msg : str
        Message to print to the terminal.
    mode : int, optional
        If mode is activated, message becomes for:
        1. an error message
    """
    if mode == 1:
        print(f"{ColorFont.red}[ERROR]{ColorFont.default} {msg}")
    else:
        print(msg)


def style(expr, args):
    """Set the output style for the terminal print.

    Parameters
    ----------
    expr : float
        Evaluated expression from the parser as float.
    args : dict
        Dictionary of the keywords and values from the parser.

    Returns
    -------
    expr: str
        Evaluated expression from the parser as str.
    """
    expr = str(expr)
    if args["color"] and args["color"] in ColorFont.__dict__:
        color = ColorFont.__dict__[args["color"]]
        expr = color + expr
    if args["bold"]:
        expr = ColorFont.bold + expr
    if args["underlined"]:
        expr = ColorFont.underlined + expr
    return expr


def bashcalc(args):
    """Evaluate the parser arguments from the command line to math expression.
    
    Returns
    -------
    args : dict
        Dictionary of the keywords and values from the parser.
    """
    result = 0
    try:
        result = Decimal(eval(args["infile"]))

        if args["round"]:
            try:
                result = round(result, args["round"])
            except InvalidOperation as e_msg:
                log_message(e_msg, mode=1)

        if args["int"]:
            result = int(result)

        if args["science"]:
            digits = args["science"]
            result = f"{result:.{digits}E}"

        result = style(result, args)

        log_message(result)
        return result
    except (NameError, TypeError, SyntaxError) as e_msg:
        log_message(e_msg, mode=1)
        sys.exit(1)


def get_args():
    """Get the parser arguments from the command line.
    
    Returns
    -------
    args : dict
        Dictionary of the keywords and values from the parser.
    """
    parser = argparse.ArgumentParser(
        description=(
            "copy or rename any file(s) to a hash-secured filename via terminal"
        )
    )
    # Arguments for loading the data
    parser.add_argument(
        "infile",
        type=str,
        help=('Write the mathematic expression like: "(2 + 4) * 3"'),
    )
    parser.add_argument(
        "-c",
        "--color",
        help=(
            "define the color of the output. The following options are available:"
            f"{ColorFont.default}default{ColorFont.default}, "
            f"{ColorFont.black}black{ColorFont.default}, "
            f"{ColorFont.red}red{ColorFont.default}, "
            f"{ColorFont.green}green{ColorFont.default}, "
            f"{ColorFont.yellow}yellow{ColorFont.default}, "
            f"{ColorFont.blue}blue{ColorFont.default}, "
            f"{ColorFont.magenta}magenta{ColorFont.default}, "
            f"{ColorFont.cyan}cyan{ColorFont.default}, "
            f"{ColorFont.lightgray}lightgray{ColorFont.default}, "
            f"{ColorFont.darkgray}darkgray{ColorFont.default}, "
            f"{ColorFont.lightred}lightred{ColorFont.default}, "
            f"{ColorFont.lightgreen}lightgreen{ColorFont.default}, "
            f"{ColorFont.lightyellow}lightyellow{ColorFont.default}, "
            f"{ColorFont.lightblue}lightblue{ColorFont.default}, "
            f"{ColorFont.lightmagenta}lightmagenta{ColorFont.default}, "
            f"{ColorFont.lightcyan}lightcyan{ColorFont.default}, "
            f"{ColorFont.white}white{ColorFont.default}"
        ),
        default=None,
        type=str,
    )
    parser.add_argument(
        "-b",
        "--bold",
        help=(f"Print {ColorFont.bold}results{ColorFont.resetall} in bold mode"),
        action="store_true",
    )
    parser.add_argument(
        "-u",
        "--underlined",
        help=(
            f"Print {ColorFont.underlined}results{ColorFont.resetunderlined} in "
            "underlined mode"
        ),
        action="store_true",
    )
    parser.add_argument(
        "-i",
        "--int",
        help=("Result will be printed as intiger-value"),
        action="store_true",
    )
    parser.add_argument(
        "-r",
        "--round",
        help=(
            "Result will be printed as rounded float-value for given number of digits"
        ),
        default=None,
        type=int,
    )
    parser.add_argument(
        "-s",
        "--science",
        help=("Result will be printed in scientific notation"),
        default=None,
        type=int,
    )
    parser.add_argument(
        "-v",
        "--version",
        help=("displays the current version of bashcalc"),
        action="store_true",
    )
    args = vars(parser.parse_args())

    return args


def command_line_runner(opt=None):
    """Run bashcalc() via command line.
    
    Parameters
    ----------
    opt : dict, optional
        Optional Dictionary for modifying the parser arguments; default is None.
    """
    args = get_args()
    # For pytest
    if opt:
        for item, value in opt.items():
            args[item] = value

    if args["version"]:
        log_message(__version__)

    if not args["infile"]:
        log_message("Missing input!", mode=1)
        return

    bashcalc(args)


if __name__ == "__main__":
    command_line_runner()
