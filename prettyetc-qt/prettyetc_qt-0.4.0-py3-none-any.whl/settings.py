#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Manage settings view."""

import abc
import os
import platform
from functools import partial

from PySide2.QtCore import QTimer
from PySide2.QtGui import QIcon
from PySide2.QtWidgets import (
    QAbstractButton, QApplication, QDialog, QMainWindow, QStyle)

from prettyetc.baseui import SettingsManager
from prettyetc.baseui.ui import BaseSettings
from prettyetc.etccore import ChildLoggerHelper

from . import themes
from .components.widgets.settings import Ui_settings
from .utils import init_qt_components

DEFAULT_SETTINGS = {
    "qtview": {
        "rootfield default view": "Tree"
    },
    "qtappearance": {
        "theme": "default",
    },
    "qtdebug": {
        "hidden actions": False,
        "enable find": False,
    },
}

__all__ = ("SettingsDialog", "SettingApplyer")


class SettingsDialogMeta(abc.ABCMeta, type(QDialog)):
    """Join QDialog metaclass to BaseSettings metaclass."""


class SettingApplyer(ChildLoggerHelper):
    """Apply settings in the whole UI."""
    loggername = "qtui.settings.applyer"

    __slots__ = ("app", "mainwindow", "settings", "stylesheets", "palettes",
                 "debug")

    def __init__(self,
                 app: QApplication,
                 mainwindow: QMainWindow,
                 settings: SettingsManager,
                 debug: bool = False):

        self.stylesheets = []
        self.palettes = []

        super().__init__()

        self.app = app
        self.mainwindow = mainwindow
        self.settings = settings
        self.debug = debug

    # first applies
    def first_apply(self, debug: bool = False):
        """
        Apply the hardcoded settings.

        These settings can depend on OS,
        environment or setup settings.
        """
        mainwindow = self.mainwindow
        self.app.setDesktopSettingsAware(True)
        self.stylesheets = themes.load_all()
        self.palettes = themes.load_palettes()

        # setup os-dependent
        if platform.system() == "Windows":
            # show the icon on app bar
            import ctypes  # pylint: disable = C0415
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(
                'prettyetc')

        if platform.system() != "Linux":
            # FIXME: Add check for X11/Wayland

            # hide on windows until an icon pack is available
            # mainwindow.toolbar_general.setVisible(False)

            # set default icons
            mainwindow.action_new.setIcon(QApplication.style().standardIcon(
                QStyle.SP_FileIcon))
            mainwindow.action_open.setIcon(QApplication.style().standardIcon(
                QStyle.SP_DialogOpenButton))
            mainwindow.action_save.setIcon(QApplication.style().standardIcon(
                QStyle.SP_DialogSaveButton))
            mainwindow.action_delete.setIcon(QApplication.style().standardIcon(
                QStyle.SP_TrashIcon))

            # use text as icon
            mainwindow.action_add.setIcon(QIcon())
            mainwindow.action_add.setText("+")

        if self.debug or debug:
            self.first_debug_apply()

    def first_debug_apply(self):
        """Same as first_apply, but for debugging purposes."""
        try:
            init_qt_components(
                os.path.join(
                    os.path.abspath("."), "prettyetc_qt", "prettyetc_qt",
                    "components"),
                languages=("en_GB", "it_IT"),
                generate_project=True,
                generate_init=False)

        except Exception as ex:  # pylint: disable=W0703
            self.logger.debug("Failed to run init_qt_components.", exc_info=ex)

    # generic appliers
    def apply(self, debug: bool = False):
        """
        Apply all the normal settings.

        These settings can be changed via the
        SettingsManager or in the settings view.
        """
        settings = self.settings
        mainwindow = self.mainwindow

        enable_find = settings.qtdebug.get("enable find", False)
        mainwindow.findview_action.setVisible(enable_find)
        # self.findview.setDisabled(not enable_find)

        # view
        self.theme_apply()

        if self.debug or debug:
            self.debug_apply()

    def debug_apply(self):
        """Same as apply, but for debugging purposes."""
        if self.settings.qtappearance.get("theme") == ".debug":
            self.logger.debug("Start debug theme auto reloading.")
            timer = QTimer(self.mainwindow)
            timer.setInterval(5000)
            timer.timeout.connect(partial(
                self.theme_apply,
                reload=True,
            ))
            timer.start()

    # specific appliers
    def theme_apply(self, reload: bool = False):
        """Apply the theme to the UI."""
        self.app.setStyleSheet("")
        self.app.setPalette(self.app.style().standardPalette())

        if reload:
            self.stylesheets = themes.load_all()
            self.palettes = themes.load_palettes()

        themename = self.settings.qtappearance.get("theme", "default")
        if themename == "default":
            self.logger.info("Set default theme")

        else:
            theme_setted = False
            for stylesheet in self.stylesheets:
                if stylesheet.name == themename:
                    self.app.setStyleSheet(stylesheet.stylesheet)
                    self.logger.info(
                        "Stylesheet theme setted to %s",
                        stylesheet.name,
                    )
                    theme_setted = True
                    break

            if not theme_setted:
                for palette in self.palettes:
                    if palette.name == themename:
                        self.app.setPalette(palette.palette)
                        self.logger.info(
                            "Palette theme setted to %s",
                            palette.name,
                        )
                        if palette.stylesheet is not None:
                            self.app.setStyleSheet(palette.stylesheet)
                        break


class SettingsDialog(
        BaseSettings, QDialog, Ui_settings, metaclass=SettingsDialogMeta):
    """Represents the main settings dialog."""

    def __init__(self, applyer: SettingApplyer, *args, **kwargs):
        super().__init__(None, *args, **kwargs)
        self.init_done = False
        self.applyer = applyer

    def init_ui(self, *args, **kwargs):
        if not self.init_done:
            self.setupUi(self)
            super().init_ui(*args, **kwargs)
            self.settings.init_default(DEFAULT_SETTINGS)

            self.show_settings_data()
            self.setting_tabs.setCurrentIndex(0)
            self.init_done = True

    def show_settings_data(self):
        """
        Assing settings values to UI.

        .. versionadded:: 0.2.0
        """
        # view
        self.view_rootfield.setCurrentText(
            str(self.data.qtview["rootfield default view"]))

        # appearance
        self.appearance_theme.clear()
        self.appearance_theme.addItem("default")
        for theme in themes.load_all() + themes.load_palettes():
            self.appearance_theme.addItem(theme.name)
        self.appearance_theme.setCurrentText(self.data.qtappearance["theme"])

        # debug
        self.debug_enable_find.setChecked(
            bool(self.data.qtdebug["enable find"]))

    def save(self, *args, **kwargs):
        """Add Qt related configs to save."""
        # view
        self.data.qtview[
            "rootfield default view"] = self.view_rootfield.currentText()

        # appearance
        self.data.qtappearance["theme"] = self.appearance_theme.currentText()

        # debug
        self.data.qtdebug["enable find"] = self.debug_enable_find.isChecked()

        super().save(*args, **kwargs)

    def handle_btnbox(self, widget: QAbstractButton):
        """Handle all the buttons in button box."""
        role = self.buttonbox.buttonRole(widget)
        if role == self.buttonbox.ResetRole:
            self.reset(DEFAULT_SETTINGS)
            self.show_settings_data()

        elif role == self.buttonbox.RejectRole:
            self.show_settings_data()

        elif role in (self.buttonbox.ApplyRole, self.buttonbox.AcceptRole):
            self.save()
            self.applyer.apply()

    def show(self):
        """Run self.show and self.exec_"""
        super().show()
        self.exec_()
