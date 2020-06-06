"""This is the Expansion API, a generative art package with high levels of abstraction,
specifically pertaining to a point(s) reproducing in an image, with changing colors, and even
environment-sensitive reproduction, with obstacles.
"""

# __init__.py for expansion package.
# Imports from module expansion.py, so that members
# can be accessed as expansion.name, rather than expansion.expansion.name.

__version__ = '1.0.2'
__author__ = 'Rajarshi Mandal'
__all__ = ['ColoredPoint',
           'ColoredPointHandler',
           'is_multiprocessing',
           'disable_multiprocessing',
           'enable_multiprocessing',
           'core_count',]

from expansion.expansion import (ColoredPoint,
                                 ColoredPointHandler,
                                 is_multiprocessing,
                                 disable_multiprocessing,
                                 enable_multiprocessing,
                                 core_count)
