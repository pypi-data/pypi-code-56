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
            self.settings.qtdebug = {}
        if "hidden actions" not in self.settings.qtdebug and hasattr(self, "debug_hidden_actions"):
            self.settings.qtdebug[
                "hidden actions"] = self.debug_hidden_actions.isChecked()

    def save(self):
        """Add Qt related configs to save."""
        self.settings.qtdebug[
            "hidden actions"] = self.debug_hidden_actions.isChecked()

        super().save()

    def accept(self, *args):
        """Apply configs."""
        self.save()
        self.apply_callback(self.settings)
        super().accept(*args)
