#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Usage: python3 -m eririn <EXCELFILE> <FILE>

Arguments:
  <EXCELFILE>    output Excel .xlsx file (with extension).
  <FILE>         input image files

Options:
  -h --help
  -v       verbose mode
"""

import os
import sys

from docopt import docopt
from . import conv as eririnlib


def main():
    arguments = docopt(__doc__)
    print(arguments)
    eririnlib.main(arguments)


main()
