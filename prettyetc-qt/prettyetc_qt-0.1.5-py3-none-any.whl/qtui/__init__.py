#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""An UI interface for the prettyetc project, powered by Qt."""

__version__ = "0.1.5"
try:
    from .main import WindowManager

    __prettyetc_ui__ = "qt"
    __main_class__ = WindowManager

    uilaunch = __main_class__.main
except ImportError:
    # running on gitlab CI
    pass
