# -*- coding: utf-8 -*-
"""Module to move files using 'dd'

This module uses dd and then rm to
1. Copy files from a src dir to a dst dir
2. Remove the files from the src dir.

Example:
    $ pydd --src /Documents/data/ --dst Documents/archive/ --regex *.dat

    This moves files that match the regex /Documents/data/*.dat to Documents/archive/
"""

import logging
import sys

from .dd import pydd
from .parser import parse_args


def set_logger_mode(quiet_mode: bool) -> None:
    """ Configure the logger to be in debug/info mode.

    :param quiet_mode: bool
        if true, configures the logger to allow only "ERROR" level logs
    :return: None
    """
    if quiet_mode:
        logging.basicConfig(format="%(levelname)s: %(message)s", level=logging.ERROR)
    else:
        logging.basicConfig(format="%(levelname)s: %(message)s", level=logging.INFO)


def main():
    args = parse_args(sys.argv[1:])
    set_logger_mode(quiet_mode=args.quiet)
    pydd(
        src_dir=args.src,
        dst_dir=args.dst,
        regex=args.regex,
        disable_progressbar=args.quiet,
    )
