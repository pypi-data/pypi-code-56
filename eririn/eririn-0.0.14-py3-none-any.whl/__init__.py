#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from docopt import docopt
from . import conv as eririnlib

def main():
    arguments = docopt(__main__.__doc__)
    print(arguments)
    eririnlib.main(arguments)
