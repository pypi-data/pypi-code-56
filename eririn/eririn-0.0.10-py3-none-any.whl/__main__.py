#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Usage: python3 -m eririn <EXCELFILE> <FILE>...

Arguments:
  <FILE>         input image files
  <EXCELFILE>    output Excel .xlsx file (with extension).

Options:
  -h --help
  -v       verbose mode
"""

import os
import sys

from docopt import docopt
from . import conv as eririnlib

if __name__ == '__main__':
    arguments = docopt(__doc__)
    print(arguments)
    eririnlib.main(arguments)

