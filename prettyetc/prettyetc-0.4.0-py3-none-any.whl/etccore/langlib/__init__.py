#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Core stuffs for managing configuration data.

The whole library is based on fields, objects that contain a name,
some data, an optional description and extra attributes if available.

.. tip::
    All submodules members are available in this namespace.
"""
from .field import *
from .field import __all__ as field_all
from .parsers import *
from .parsers import __all__ as parsers_all
from .root import *
from .root import __all__ as root_all
from .serializers import *
from .serializers import __all__ as serializers_all

__all__ = field_all + parsers_all + serializers_all + root_all
