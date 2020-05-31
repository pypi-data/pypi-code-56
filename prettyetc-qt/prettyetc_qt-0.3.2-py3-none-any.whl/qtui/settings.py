#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Manage settings view."""

# pylint: disable=E0237
import abc

from prettyetc.baseui.ui.settings import BaseSettings
from PySide2.QtWidgets import QAbstractButton, QDialog

from . import themes
from .components.widgets.settings import Ui_settings

DEFAULT_VALUE = {
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

__all__ = ("SettingsDialog", )


class SettingsDialogMeta(abc.ABCMeta, type(QDialog)):
    """Join QDialog metaclass to BaseSettings metaclass."""


class SettingsDialog(
        BaseSettings, QDialog, Ui_settings, metaclass=SettingsDialogMeta):
    """Represents the main settings dialog."""

    def __init__(self, *args, **kwargs):
        super().__init__(None, *args, **kwargs)
        self.init_done = False

    def init_ui(self, *args, **kwargs):
        if not self.init_done:
            self.setupUi(self)
            super().init_ui(*args, **kwargs)
            self.settings.init_default(DEFAULT_VALUE)

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
        self.debug_hidden_actions.setChecked(
            bool(self.data.qtdebug["hidden actions"]))
        self.debug_enable_find.setChecked(bool(self.data.qtdebug["enable find"]))

    def save(self, *args, **kwargs):
        """Add Qt related configs to save."""
        # view
        self.data.qtview[
            "rootfield default view"] = self.view_rootfield.currentText()

        # appearance
        self.data.qtappearance["theme"] = self.appearance_theme.currentText()

        # debug
        self.data.qtdebug[
            "hidden actions"] = self.debug_hidden_actions.isChecked()
        self.data.qtdebug["enable find"] = self.debug_enable_find.isChecked()

        super().save(*args, **kwargs)

    def handle_btnbox(self, widget: QAbstractButton):
        """Handle all the buttons in button box."""
        role = self.buttonbox.buttonRole(widget)
        if role == self.buttonbox.ResetRole:
            self.reset(DEFAULT_VALUE)
            self.show_settings_data()

        elif role == self.buttonbox.RejectRole:
            self.show_settings_data()

    def show(self):
        """Run self.show and self.exec_"""
        super().show()
        self.exec_()
