#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Manage main interfaces."""

import abc
import logging
import os
import platform
import sys
import threading
from functools import partial

from prettyetc.baseui import main as basemain
from prettyetc.baseui.utils import read_autoselect
from prettyetc.etccore import __version__ as etccore_version
from prettyetc.etccore.langlib.parsers import BadInput
from prettyetc.etccore.langlib.root import RootField
from PySide2 import __version__ as pyside2_version
from PySide2.QtCore import QPoint
from PySide2.QtCore import __version__ as qt_version
from PySide2.QtWidgets import (QApplication, QErrorMessage, QFileDialog,
                               QMainWindow, QMessageBox, QStyleFactory,
                               QToolTip, QWidget)

from . import __version__ as qtui_version
from . import themes
from .components.widgets.find import Ui_findAction
from .components.widgets.mainwindow import Ui_MainWindow
# try relative imports
from .containers import ConfTab
from .settings import SettingsDialog
from .utils import get_main_window, init_qt_components, to_action, tr, show_tooltip

__all__ = ("WindowManager", )


class WindowManagerMeta(abc.ABCMeta, type(QMainWindow)):
    """Join QMainWindow metaclass to BaseMainUi metaclass."""


class WindowManager(
        basemain.BaseMainUi,
        Ui_MainWindow,
        QMainWindow,
        metaclass=WindowManagerMeta):
    """Manage main window."""

    loggername = "qtui.mainui.window"

    def __init__(self, *args, **kwargs):
        # utils.load_qt_plugins()
        self.app = QApplication(sys.argv)
        self.app.setDesktopSettingsAware(True)

        self.configs_tabs = None
        self.stylesheets = []
        self.palettes = []

        super().__init__(*args, **kwargs)

        self.logger.info("Avaiable QT styles: %s",
                         " ".join(QStyleFactory.keys()))

        self.read_file = partial(self._read_callback, self.read_file)

        self.settings_dialog = SettingsDialog(parent=self)
        self.findview_action = to_action(FindView(parent=self))

    def _read_callback(self, original_clb, *args, **kwargs):
        """Call the original callback and process the result."""

        # partial restore of the deprecated behaviour

        res = original_clb(*args, **kwargs)
        read_autoselect(res, self.add_tab, self.handle_badinput)

    # from common ui
    def init_ui(self):
        """Call internal initializer with qt dependent arguments and init mainwindow."""
        if self.logger.isEnabledFor(logging.DEBUG):
            try:
                init_qt_components(
                    os.path.abspath("prettyetc/qtui/components/"),
                    languages=("en_GB", "it_IT"),
                    generate_project=True,
                    generate_init=False)

            except Exception as ex:  # pylint: disable=W0703
                self.logger.debug(
                    "Failed to run _init_qt_components.", exc_info=ex)

        self.setupUi(self)

        # setup configs
        self.settings_dialog.init_ui()

        self.stylesheets = themes.load_all()
        self.palettes = themes.load_palettes()

        self.apply_configs(self.settings_dialog.settings)

        # setup toolbar actions
        self.toolbar.addAction(self.findview_action)

        # setup tab widget
        # DO NOT CHANGE THE ORDER OF THE FOLLOWING LINES
        conf_tabs = ConfTab()
        self.rootLayout.replaceWidget(self.configs_tabs, conf_tabs)
        conf_tabs.copy_properties(self.configs_tabs)
        self.configs_tabs.setParent(None)
        self.configs_tabs = conf_tabs

        # setup status bar
        # statusbar = self.statusbar

        # setup os-dependent
        if platform.system() == "Windows":
            self.toolbar.removeAction(self.action_new)
            self.toolbar.removeAction(self.action_save)
            self.toolbar.removeAction(self.action_saveas)
            self.toolbar.removeAction(self.action_open)
            self.toolbar.removeAction(self.action_preferences)
            # self.toolbar.setVisible(False)

    def show(self):
        """Run QMainWindow.show and self.app.exec()"""
        QMainWindow.show(self)
        self.app.exec_()

    def close(self):
        """
        Save settings before close.

        .. versionadded:: 0.2.0
        """
        try:
            # if settings never shows, the save fails
            self.settings_dialog.close()
        except AttributeError:
            pass
        # self.app.closeAllWindows()
        super().close()

    # extra configs
    def add_tab(self, rootfield: RootField):
        """Add new rootfield to configs_tabs."""
        self.logger.debug("Add rootfield %s to conf tabs", rootfield.name)
        self.configs_tabs += rootfield

    def handle_badinput(self, ex: BadInput):
        """Show error dialog with the error."""

        dialog = QErrorMessage(self)
        dialog.setObjectName("openErrorDialog")
        dialog.setWindowTitle("{}: {}".format(
            self.app.translate("openErrorDialog", "Failed to open file"),
            os.path.split(ex.filename)[1]))
        dialog.showMessage(repr(ex))

    def apply_configs(self, settings):
        """Apply configs given from settings."""

        # debug
        if settings.qtdebug.get("hidden actions", False):
            self.logger.debug("Show hidden actions")
            self.action_new.setDisabled(False)
            self.action_save.setDisabled(False)
            self.action_saveas.setDisabled(False)
        else:
            self.logger.debug("Hide hidden actions")
            self.action_new.setDisabled(True)
            self.action_save.setDisabled(True)
            self.action_saveas.setDisabled(True)

        enable_find = settings.qtdebug.get("enable find", False)
        self.findview_action.setVisible(enable_find)
        # self.findview.setDisabled(not enable_find)
        # view
        self.app.setStyleSheet("")
        self.app.setPalette(self.app.style().standardPalette())

        themename = settings.qtappearance.get("theme", "default")
        if themename == "default":
            self.logger.info("Set default theme")
        else:
            theme_setted = False
            for stylesheet in self.stylesheets:
                if stylesheet.name == themename:
                    self.app.setStyleSheet(stylesheet.stylesheet)
                    self.logger.info("Stylesheet theme setted to %s",
                                     stylesheet.name)
                    theme_setted = True
                    break

            if not theme_setted:
                for palette in self.palettes:
                    if palette.name == themename:
                        self.app.setPalette(palette.palette)
                        self.logger.info("Palette theme setted to %s",
                                         palette.name)
                        if palette.stylesheet is not None:
                            self.app.setStyleSheet(palette.stylesheet)
                        break

    # slots
    def open_confile(self, *_):
        """Called when open action is fired, it opens a file input dialog."""
        filename, _ = QFileDialog.getOpenFileName(
            self,
            "Select a config file",
            options=QFileDialog.DontUseNativeDialog)
        if os.path.isfile(filename):
            self.read_file(filename)

    def open_settings(self, *_):
        """Called when setting action is fired, it opens the settings dialog."""
        self.settings_dialog.run()
        self.apply_configs(self.settings_dialog.settings)
        self.settings_dialog.setParent(None)
        self.settings_dialog = SettingsDialog(parent=self)
        self.settings_dialog.init_ui()

    def open_about(self, *_):
        """Open the standard Qt about and show summary informations and library versions."""
        try:
            import homebase
        except ImportError:
            homebase = None

        message = (
            "See your configuration file using a pretty and universal interface.\n\n"
            "© Copyright 2019, trollodel.\n"
            "This Qt UI for prettyetc version {}.\n\n"
            "Used libraries:\n"
            "The etccore library (formally named as prettyetc) version {}.\n\n"
            "3rd part libraries:\n"
            "The PySide2 python binding for the Qt framework version {}.\n"
            "The Qt framework version {}.\n".format(
                qtui_version, etccore_version, pyside2_version, qt_version))

        if homebase is not None:
            message += "The homebase library version {}.\n".format(
                homebase.__version__)

        QMessageBox.about(self, "The prettyetc project\n", message)

    def status_changed(self):
        """Change the status bar."""

    @staticmethod
    def main(*args, **kwargs):
        """Launch qtui, if avaiable."""
        basemain.UiLauncher.main(*args, preferred_uis=("qt", ), **kwargs)


class FindView(Ui_findAction, QWidget):
    """Find view and manager."""

    FINDTYPE_VALUES = ("all", "name", "data", "description")

    def __init__(self, *args, **kwargs):
        super(FindView, self).__init__(*args, **kwargs)
        self._find_active = None
        self.setupUi(self)

        self.find.clicked.connect(self.do_find)
        self.text.editingFinished.connect(self.do_find)

        self.findtype.editTextChanged.connect(self.restore_find)
        self.text.textEdited.connect(self.restore_find)

    def do_find(self, *_):
        """Find the string in the current root field (using find_by_attr)."""
        self.restore_find()
        mainwindow = get_main_window()
        conftab = mainwindow.configs_tabs
        current_tab = conftab.currentWidget()
        index = self.findtype.currentIndex()
        text = self.text.text()
        if text:
            self._find_active = current_tab.find(
                text, FindView.FINDTYPE_VALUES[index])
            if not self._find_active:
                show_tooltip(self.text, tr("FindView", "No field found"), timeout=10)
        else:
            show_tooltip(self.text, tr("FindView", "Please insert some text to find"))


    def restore_find(self, *_):
        """Restore fields state if a find operators is running successfully."""
        if self._find_active:
            for field in self._find_active:
                field.dispatch(False, "highlight")
            self._find_active = None
