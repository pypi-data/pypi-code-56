#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Built-in qt stylesheets manager."""

import inspect
import os

from prettyetc.etccore.logger import ChildLoggerHelper
from PySide2.QtCore import Qt
from PySide2.QtGui import QColor, QPalette

__all__ = ("QtTheme", "load_all", "load_palettes")


class QtTheme(ChildLoggerHelper):
    """
    Representation of a theme file.

    This class is made to contains all the necessary informations for qt and
    a name system.
    """

    __slots__ = ("stylesheet", "name", "package", "logger", "dirpath",
                 "palette")
    loggername = "qtui.themes"

    def __init__(self,
                 fullpath: str,
                 basepath: str = None,
                 palette: QPalette = None):
        super(QtTheme, self).__init__()
        self.palette = palette
        if fullpath is None:
            self.stylesheet = None
            self.name = None
            self.package = None
            self.dirpath = os.path.dirname(
                inspect.getfile(inspect.currentframe()))

        else:
            self.dirpath, filename = os.path.split(fullpath)

            if basepath is None:
                basepath = os.path.dirname(
                    inspect.getfile(inspect.currentframe()))

            path = os.path.relpath(self.dirpath, basepath)
            self.name = filename.split(".", 1)[0]
            self.package = os.path.join(os.path.basename(basepath),
                                        path).replace(os.path.sep, ".")

            try:
                with open(fullpath) as stream:
                    self.stylesheet = stream.read()
            except IOError as ex:
                self.logger.error(
                    "Failed to read stylesheet from path %s\nBelow the traceback:",
                    fullpath,
                    exc_info=ex)

    def from_package(self, name: str, extension: str = "qss"):
        """Load stylesheets from current package."""
        path = os.path.join(self.dirpath, "{}.{}".format(name, extension))
        stylesheet = QtTheme(path, self.package.replace(".", os.path.sep))

        return stylesheet

    def __str__(self):
        """Return the stylesheet."""
        return str(self.stylesheet)


def load_palettes(reset=False) -> list:
    """Load QPalette objects (hardcoded)."""
    if load_palettes.cache is None or reset:
        themes = []
        # https://gist.github.com/QuantumCD/6245215

        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(53, 53, 53))
        palette.setColor(QPalette.WindowText, Qt.white)
        palette.setColor(QPalette.Base, QColor(25, 25, 25))
        palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
        palette.setColor(QPalette.ToolTipBase, Qt.white)
        palette.setColor(QPalette.ToolTipText, Qt.white)
        palette.setColor(QPalette.Text, Qt.white)
        palette.setColor(QPalette.Button, QColor(53, 53, 53))
        palette.setColor(QPalette.ButtonText, Qt.white)
        palette.setColor(QPalette.BrightText, Qt.red)
        palette.setColor(QPalette.Link, QColor(42, 130, 218))

        palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
        palette.setColor(QPalette.HighlightedText, Qt.black)

        theme = QtTheme(None, palette=palette)
        theme.name = "Dark fusion"
        theme.package = "QuantumCD"
        theme.stylesheet = "QToolTip { color: #ffffff; background-color: #2a82da; border: 1px solid white; }"
        themes.append(theme)

        # last instruction
        load_palettes.cache = themes

    return load_palettes.cache


load_palettes.cache = None


def load_all(reset=False) -> list:
    """Load all qss files in this directory and save it in a list of QtTheme objects."""
    if load_all.cache is None or reset:
        basepath = os.path.dirname(inspect.getfile(inspect.currentframe()))
        stylesheets = []
        for directory, _, files in os.walk(basepath):
            for file in files:
                if file.endswith(".qss"):
                    stylesheets.append(QtTheme(os.path.join(directory, file)))
        load_all.cache = stylesheets

    return load_all.cache


load_all.cache = None
