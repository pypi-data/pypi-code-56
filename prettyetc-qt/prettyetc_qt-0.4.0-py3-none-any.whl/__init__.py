#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""An UI interface for the prettyetc project, powered by Qt."""

__version__ = "0.4.0"
import sys

try:
    import PySide2.QtWidgets

except ImportError:
    # running on gitlab CI
    print("PySide2 library is not available.", file=sys.stderr)

else:
    from .main import WindowManager
    __prettyetc_ui__ = "qt"
    __main_class__ = WindowManager

    uilaunch = __main_class__.main
