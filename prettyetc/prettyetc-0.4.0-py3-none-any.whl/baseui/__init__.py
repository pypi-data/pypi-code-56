#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This module provides stuffs to create quickly an
interface for managing configuration files and root fields.

It has lots of helper classes and functions for initializing all required stuffs for you.

.. tip::
    All submodules members are available in this namespace.
"""

from .cmdargs import *
from .cmdargs import __all__ as cmdargs_all
from .main import *
from .main import __all__ as main_all
from .settings import *
from .settings import __all__ as settings_all
from .ui import *
from .ui import __all__ as ui_all
from .utils import *
from .utils import __all__ as utils_all

uilaunch = UiLauncher.main

__all__ = (
    "uilaunch",) + cmdargs_all + main_all + settings_all + ui_all + utils_all
