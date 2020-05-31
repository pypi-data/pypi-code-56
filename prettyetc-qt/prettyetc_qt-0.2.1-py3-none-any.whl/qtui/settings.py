#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Manage settings view."""

# pylint: disable=E0237

from PySide2.QtWidgets import QDialog

from prettyetc.baseui.settings import BaseSettingsUi

from .components.widgets.settings import Ui_settings


class SettingsDialog(BaseSettingsUi, QDialog, Ui_settings):
    """Represents the main settings dialog."""

    def __init__(self, *args, apply_callback=lambda *args: None, **kwargs):
        super().__init__("default", *args, **kwargs)
        self.setupUi(self)
        self.apply_callback = apply_callback
        self.show_settings_data()

        # this configuration is useless.
        self.debug_custom_style_sheet_label.setText("Useless (stylesheet)")

    def init_config(self):
        """Init qt configs."""
        super().init_config()
        if not hasattr(self.settings, "qtgeneral"):
            self.settings.qtgeneral = {}
        if not hasattr(self.settings, "qtparsing"):
            self.settings.qtparsing = {}
        if not hasattr(self.settings, "qtwriting"):
            self.settings.qtwriting = {}
        if not hasattr(self.settings, "qtadvanced"):
            self.settings.qtadvanced = {}
        if not hasattr(self.settings, "qtdebug"):
            self.settings.qtdebug = {"hidden actions": False, "stylesheet": ""}

    def load(self, *args, **kwargs):
        """
        Load data and call :meth:`~SettingsDialog.show_settings_data`.

        .. versionadded:: 0.2.0
        """
        super().load(*args, **kwargs)
        self.show_settings_data()

    def show_settings_data(self):
        """
        Assing settings values to UI.

        .. versionadded:: 0.2.0
        """

        self.debug_hidden_actions.setChecked(
            bool(self.settings.qtdebug.get("hidden actions", False)))
        self.debug_custom_style_sheet.setText(
            str(self.settings.qtdebug.get("stylesheet", "")))

    def save(self):
        """Add Qt related configs to save."""
        self.settings.qtdebug[
            "hidden actions"] = self.debug_hidden_actions.isChecked()
        self.settings.qtdebug[
            "stylesheet"] = self.debug_custom_style_sheet.text()

        super().save()

    def accept(self, *args):
        """Apply configs."""
        self.save()
        self.apply_callback(self.settings)
        super().accept(*args)
