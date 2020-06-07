#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""All code containers."""
import os.path
from functools import partial

from PySide2.QtCore import Qt, QTimer
from PySide2.QtGui import QKeySequence
from PySide2.QtWidgets import QMessageBox, QShortcut, QTabWidget

from prettyetc.baseui import SettingsManager
from prettyetc.etccore.langlib import RootField

from .fieldviews import CommonFieldView, CompositeFieldView
from .utils import get_main_window, tr

__all__ = ("ConfTab",)


class ConfTab(QTabWidget):
    """Display and manage the main view of configs (by tab widget)."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setObjectName("conftab")
        self.tabCloseRequested.connect(self.on_tab_close)

        self.currentChanged.connect(self.show_filename_status)
        self.settings = SettingsManager.factory(None)

        # TODO: use settings for shortcuts
        self.shortcuts = [
            (QShortcut(QKeySequence(Qt.CTRL + Qt.Key_W), self),
             lambda: self.tabCloseRequested.emit(self.currentIndex())),
        ]

        for shortcut, slot in self.shortcuts:
            shortcut.activated.connect(slot)

    def __add__(self, root):
        """A shortcut for the add_* method."""
        if isinstance(root, CommonFieldView):
            self.addTab(root)
        elif isinstance(root, RootField):
            QTimer.singleShot(1, partial(self.add_rootfield, root))
        else:
            raise TypeError(
                "unsupported operand type(s) for +: '{}' and '{}'".format(
                    type(self).__name__,
                    type(root).__name__,
                ))
        return self

    def copy_properties(self, tabwidget):
        """Copy property to self from given tabwidget."""
        self.setUsesScrollButtons(tabwidget.usesScrollButtons())
        self.setTabBarAutoHide(tabwidget.tabBarAutoHide())
        self.setTabsClosable(tabwidget.tabsClosable())
        self.setDocumentMode(tabwidget.documentMode())
        self.setTabPosition(tabwidget.tabPosition())
        self.setElideMode(tabwidget.elideMode())
        self.setTabShape(tabwidget.tabShape())
        self.setMovable(tabwidget.isMovable())
        self.setStyleSheet(tabwidget.styleSheet())

    def addTab(self, tab):
        """Add checks to new tab."""
        if tab.rootfield.name is None:
            checked = (None, None)
        else:
            checked = self.check_duplicates(tab)

        if checked[0] is True:
            self.setCurrentIndex(checked[1])
        else:
            index = super().addTab(tab, "")
            self.setCurrentIndex(index)
            self.update_current_tab()

    def add_rootfield(self, root: RootField):
        """Add new field root and create a ConfView object, by given rootfield."""
        tab = CompositeFieldView(root)
        self.addTab(tab)

        tab.run(blocking=False)

    def check_duplicates(self, tab):
        """
        Check if tabname is already in tabs.

        Return True if a tab has the same name.
        Return a list of tuple that contains the different tab and the common path head.

        .. todo::
            Finish this method
        """
        diffchildren = []
        tabpath, tabtail = os.path.split(tab.rootfield.name)
        for i in range(self.count()):
            child = self.widget(i)
            childpath, childtail = os.path.split(child.rootfield.name)
            if tabtail == childtail:
                if tabpath == childpath:
                    return (True, i)
                diffchildren.append(child)

        # for child in diffchildren
        #     common = os.path.commonprefix((tab.root.name, child.root.name))
        #     if common != tab.root.name:
        #         diffchildren.append((child, common))
        return (None, None)

    def on_tab_close(self, index: int, *_):
        """Called when tab is closing."""
        if index != -1:
            tab = self.widget(index)
            self.setCurrentIndex(index)

            objname = self.objectName()
            question_dialog = QMessageBox()

            # TODO: make some changed checks
            if tab.rootfield.name is None and not tab.rootfield:
                self.removeTab(index)
                tab.close()

            else:
                # from https://doc.qt.io/qt-5/qmessagebox.html#details
                question_dialog.setWindowTitle(tr(
                    objname,
                    "Unsaved changes",
                ))
                question_dialog.setText(
                    tr(
                        objname,
                        "The document has been modified",
                    ))
                question_dialog.setInformativeText(
                    tr(
                        objname,
                        "Do you want to save your changes?",
                    ))
                question_dialog.setStandardButtons(QMessageBox.Save |
                                                   QMessageBox.Discard |
                                                   QMessageBox.Cancel)
                ret = question_dialog.exec_()

                # check result
                if ret != QMessageBox.Cancel:
                    if ret == QMessageBox.Save:
                        self.parent().save()

                    self.removeTab(index)
                    tab.close()

    def show_filename_status(self, index: int):
        """Add message to mainwindow statusbar."""
        if index != -1:
            tab = self.widget(index)
            mainwindow = get_main_window()
            if tab.rootfield.name is None:
                mainwindow.setWindowTitle(
                    tr("conftab", "Untitled") + " — " + "Prettyetc")
            else:
                directory, filename = os.path.split(tab.rootfield.name)
                mainwindow.setWindowTitle(filename + " — " + directory + " — " +
                                          "Prettyetc")
                # mainwindow.statusbar.showMessage(tab.rootfield.name)
        else:
            mainwindow = get_main_window()
            mainwindow.setWindowTitle("Prettyetc")

    def update_current_tab(self):
        """Update current tab using the rootfield."""
        current_index = self.currentIndex()
        if current_index != -1:
            tab = self.widget(current_index)
            tabname = tr(
                "conftab",
                "Untitled",
            ) if tab.rootfield.name is None else os.path.split(
                tab.rootfield.name)[1]

            self.setTabText(current_index, tabname)
            self.setTabToolTip(current_index, tab.rootfield.description)
            self.show_filename_status(current_index)

            if callable(getattr(tab, "reload", None)):
                try:
                    tab.reload()
                except KeyError:
                    pass
