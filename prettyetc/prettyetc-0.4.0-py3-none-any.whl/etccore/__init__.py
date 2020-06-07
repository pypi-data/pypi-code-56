#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Core library for processing, manipulating and writing configuration files, with some extra stuffs.

Content of this package:

- the langlib package.
  This contains all required stuff to config processing,
  including the definitions of :class:`~prettyetc.etccore.langlib.field.Field`

- the langs folder

 This folder contains all plugins shipped with this core
 Some of this is work in progress or never started.

- other modules

 These modules do stuffs to help or complete the core and
 help the UIs to showing configuration file quickly.

.. tip::
    All submodules members are available in this namespace.

.. tip::
    If you are looking for a specific member in docs, use the search page
    because the members are located in submodules.
"""

__version__ = "0.4.0"

from .confmgr import *
from .confmgr import __all__ as confmgr_all
from .langlib import *
from .langlib import __all__ as langlib_all
from .logger import *
from .logger import __all__ as logger_all
from .plugins import *
from .plugins import __all__ as plugins_all

__all__ = (
    "__version__",) + confmgr_all + langlib_all + logger_all + plugins_all
