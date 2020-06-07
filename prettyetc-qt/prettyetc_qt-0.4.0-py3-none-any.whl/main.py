#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Manage main qt interface."""
import abc
import logging
import os
import sys
from functools import partial
from string import Template

from PySide2 import __version__ as pyside2_version
from PySide2.QtCore import __version__ as qt_version
from PySide2.QtWidgets import (
    QApplication, QDialog, QErrorMessage, QFileDialog, QMainWindow, QMenu,
    QStyleFactory, QWidget)

from prettyetc.baseui import read_autoselect
from prettyetc.baseui.ui import BaseMain, CommonComponent
from prettyetc.etccore import __version__ as etccore_version
from prettyetc.etccore.langlib import BadInput, RootField, SerializeFailed

from . import __version__ as qtui_version
from .components.widgets.about import Ui_About
from .components.widgets.find import Ui_findAction
from .components.widgets.mainwindow import Ui_MainWindow
# try relative imports
from .containers import ConfTab
from .settings import SettingApplyer, SettingsDialog
from .utils import (
    get_main_window, load_qt_plugins, replace_widget, show_tooltip, to_action,
    tr)

try:
    from lark import __version__ as lark_version
except ImportError:
    lark_version = "not installed"

try:
    from homebase import __version__ as homebase_version
except ImportError:
    homebase_version = "not installed"

try:
    from ruamel.yaml import __version__ as ruamel_version
except ImportError:
    ruamel_version = "not installed"

__all__ = ("WindowManager", "uilaunch")


class WindowManagerMeta(abc.ABCMeta, type(QMainWindow)):
    """Join QMainWindow metaclass to BaseMainUi metaclass."""


class AboutDialogMeta(abc.ABCMeta, type(QMainWindow)):
    """Join Qdialog metaclass to CommonComponent metaclass."""


class WindowManager(
        BaseMain, Ui_MainWindow, QMainWindow, metaclass=WindowManagerMeta):
    """Manage main window."""

    loggername = "qtui.mainui.window"
    uiname = "qt"

    @classmethod
    def main(cls, *args, **kwargs):
        super().main(*args, ui_cls=cls, **kwargs)

    def __init__(self, *args, **kwargs):
        # when qt wants to collaborate
        load_qt_plugins("nope")

        self.app = QApplication(sys.argv)

        self.tabs = None

        super().__init__(*args, **kwargs)

        self.logger.info("Avaiable QT styles: %s",
                         " ".join(QStyleFactory.keys()))

        self._settings_applyer = SettingApplyer(
            self.app,
            self,
            None,
            debug=self.logger.isEnabledFor(logging.DEBUG),
        )
        self.read_file = partial(self._read_callback, self.read_file)

        self.settings_dialog = SettingsDialog(
            self._settings_applyer, parent=self)
        self.about_dialog = AboutDialog(parent=self)
        self.findview_action = to_action(FindView(parent=self))

    def _read_callback(self, original_clb: callable, *args, **kwargs):
        """Call the original callback and process the result."""

        # partial restore of the deprecated behaviour

        res = original_clb(*args, **kwargs)
        read_autoselect(res, self.add_tab, self.handle_badinput)

    @property
    def current_view(self) -> QWidget:
        """Get the current view (an instance of CommonFieldView)."""
        current_index = self.tabs.currentIndex()
        if current_index == -1:
            return None

        return self.tabs.widget(current_index)

    # from common ui
    def init_ui(self):
        """Call internal initializer with qt dependent arguments and init mainwindow."""
        # construct GUI
        self.setupUi(self)
        self.settings_dialog.init_ui()
        self.about_dialog.init_ui()

        # first settings setup
        self._settings_applyer.first_apply()

        # setup toolbar actions
        self.toolbar_edit.addAction(self.findview_action)

        # setup tab widget
        # DO NOT CHANGE THE ORDER OF THE FOLLOWING LINES
        conf_tabs = replace_widget(
            self.rootLayout,
            self.tabs,
            ConfTab(),
        )
        conf_tabs.copy_properties(self.tabs)
        self.tabs = conf_tabs

        # setup status bar
        # statusbar = self.statusbar

        # standard settings setup
        self._settings_applyer.settings = self.settings_dialog.settings
        self._settings_applyer.apply()

    def show(self):
        """Run QMainWindow.show and self.app.exec()"""
        # self.toolbar.setVisible(True)
        QMainWindow.show(self)
        self.app.exec_()

    def close(self):
        """Save settings before close."""

        try:
            # if the settings dialog never shows,
            # the save will fail
            self.settings_dialog.close()
        except AttributeError:
            pass

        # self.app.closeAllWindows()
        super().close()

    # handle configs I/O
    def add_tab(self, rootfield: RootField):
        """Add new rootfield to tabs."""
        self.logger.debug(
            "Add rootfield %s to conf tabs",
            rootfield.name,
        )
        self.tabs += rootfield

    def handle_badinput(self, ex: BadInput):
        """Show error dialog with the error."""

        dialog = QErrorMessage(self)
        dialog.setObjectName("BadInput_dialog")
        dialog.setWindowTitle("{}: {}".format(
            tr(
                dialog.objectName(),
                "Failed to open file",
            ),
            os.path.split(ex.filename)[1],
        ))
        dialog.showMessage(repr(ex))

    # slots
    def new(self):
        """Create an empty field."""
        rootfield = RootField(None, data=[])
        self.add_tab(rootfield)

    def save(self):
        """Save current file."""
        view = self.current_view
        if view is not None:
            if view.rootfield.name is None:
                self.open_saveas()
            else:
                try:
                    self.write_file(view.rootfield)
                except SerializeFailed as ex:
                    dialog = QErrorMessage(self)
                    dialog.setObjectName("BadInput_dialog")
                    dialog.setWindowTitle("{}: {}".format(
                        tr(
                            dialog.objectName(),
                            "Failed to open file",
                        ),
                        os.path.split(ex.filename)[1],
                    ))
                    dialog.showMessage(repr(ex))
                else:
                    view.reload()

    def open_saveas(self):
        """Open a file dialog and save the file."""
        view = self.current_view
        root = view.rootfield
        if view is not None:
            all_suffixes = self.configfactory.all_language_suffixes(
                "serializer")
            filters = []
            objname = self.objectName()
            default_filter = ""

            for language, suffixes in all_suffixes:
                cur_filter = "{} ({})".format(
                    tr(objname, language.title()),
                    " ".join("*" + suffix for suffix in suffixes),
                )
                if root.attributes["langname"] == language:
                    default_filter = cur_filter
                filters.append(cur_filter)

            filters = set(filters)

            filename, selected_filter = QFileDialog.getSaveFileName(
                self,
                caption=tr(objname, "Save file"),
                filter=";;".join(filters),
                dir="" if root.name is None else root.name,
                selectedFilter=default_filter,
                # options=QFileDialog.DontUseNativeDialog,
            )
            # override = os.path.isfile(filename)
            if filename:
                language = selected_filter.split("(")[0].strip()
                try:
                    self.write_file(
                        root,
                        filename,
                        language,
                    )

                except SerializeFailed as ex:
                    dialog = QErrorMessage(self)
                    dialog.setObjectName("SerializeFailed_dialog")
                    dialog.setWindowTitle("{}: {}".format(
                        tr(
                            "SerializeFailed_dialog",
                            "Failed to write file",
                        ),
                        os.path.split(ex.filename)[1],
                    ))
                    dialog.showMessage(repr(ex))

                else:
                    # update root with the new path and language, if any
                    if root.name != filename:
                        root.name = filename

                    if root.attributes["langname"] != language:
                        root.attributes["langname"] = language

                    self.tabs.update_current_tab()

    def open_confile(self, *_):
        """Called when open action is fired, it opens a file input dialog."""
        filename, _ = QFileDialog.getOpenFileName(
            self,
            "Select a config file",
            options=QFileDialog.DontUseNativeDialog,
        )
        if os.path.isfile(filename):
            self.read_file(filename)

    def open_settings(self, *_):
        """
        Called when setting action is fired.

        It opens the settings dialog.
        """
        self.settings_dialog.show()

    def open_about(self, *_):
        """Open the standard Qt about and show summary information and library versions."""
        if not self.about_dialog.isVisible():
            self.about_dialog.show()
        # message = (
        #     "See your configuration file using a pretty and universal interface.\n\n"
        #     "© Copyright 2019, trollodel.\n"
        #     "Prettyetc UI version {}.\n"
        #     "Prettyetc core library version {}.\n\n"
        #     "3rd party libraries:\n"
        #     "The PySide2 python binding for the Qt framework version {}.\n"
        #     "The Qt framework version {}.\n".format(
        #         qtui_version,
        #         etccore_version,
        #         pyside2_version,
        #         qt_version,
        #     ))
        #
        # if homebase is not None:
        #     message += "The homebase library version {}.\n".format(
        #         homebase.__version__)
        #
        # QMessageBox.about(
        #     self,
        #     "The prettyetc project\n",
        #     message,
        # )

    def status_changed(self):
        """Change the status bar."""

    # qt patchs
    def createPopupMenu(self) -> QMenu:
        """Suppress the toolbar QMenu selector."""
        return None


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
        conftab = mainwindow.tabs
        current_tab = conftab.currentWidget()
        index = self.findtype.currentIndex()
        text = self.text.text()
        if text:
            self._find_active = current_tab.find(
                text, FindView.FINDTYPE_VALUES[index])
            if not self._find_active:
                show_tooltip(
                    self.text,
                    tr("FindView", "No field found"),
                    timeout=10,
                )
        else:
            show_tooltip(
                self.text,
                tr("FindView", "Please insert some text to find"),
            )

    def restore_find(self, *_):
        """Restore fields state if a find operators is running successfully."""
        if self._find_active:
            for field in self._find_active:
                field.dispatch(False, "highlight")
            self._find_active = None


class AboutDialog(
        QDialog, CommonComponent, Ui_About, metaclass=AboutDialogMeta):
    """Show an about dialog with some Prettyetc information."""

    def init_ui(self):
        self.setupUi(self)
        self.info_label.setText(
            Template(self.info_label.text()).safe_substitute(
                prettyetc_ui=qtui_version,
                prettyetc=etccore_version,
            ))
        self.lib_label.setText(
            Template(self.lib_label.text()).safe_substitute(
                qt=qt_version,
                pyside2=pyside2_version,
                homebase=homebase_version,
                lark=lark_version,
                ruamel=ruamel_version,
            ))

    def close(self):
        self.hide()
