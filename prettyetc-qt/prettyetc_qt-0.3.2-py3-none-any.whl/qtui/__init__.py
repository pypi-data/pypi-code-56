#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""An UI interface for the prettyetc project, powered by Qt."""

__version__ = "0.3.2"
import sys

try:
    import PySide2.QtWidgets

except ImportError:
    # running on gitlab CI
    print("PySide2 library is not avaiable.", file=sys.stderr)

else:
    from .main import WindowManager
    __prettyetc_ui__ = "qt"
    __main_class__ = WindowManager

    uilaunch = __main_class__.main
