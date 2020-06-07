#!/usr/bin/env python3
# -*- coding: utf-8 -*-

try:
    from lark import Lark
except ImportError:
    __all__ = ()
else:
    from .sep import *
    from .sep import __all__ as sep_all
    from .space import *
    from .space import __all__ as space_all

    __all__ = sep_all + space_all
