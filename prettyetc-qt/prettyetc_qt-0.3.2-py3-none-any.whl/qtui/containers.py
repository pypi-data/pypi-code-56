#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""All code containers."""
import os.path

from prettyetc.etccore.langlib.root import RootField
from PySide2.QtWidgets import QTabWidget

from .fieldviews import CommonFieldView, CompositeFieldView
from .utils import get_main_window
__all__ = ("ConfTab", )


class ConfTab(QTabWidget):
    """Display and manage the main view of configs (by tab widget)."""

    rootConfs = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tabCloseRequested.connect(self.on_tab_close)
        self.currentChanged.connect(self.show_filename_status)

    def __add__(self, root):
        """A shortcut for the add_* method."""
        if isinstance(root, CommonFieldView):
            self.addTab(root)
        elif isinstance(root, RootField):
            self.add_rootfield(root)
        else:
            raise TypeError(
                "unsupported operand type(s) for +: '{}' and '{}'".format(
                    type(self).__name__,
                    type(root).__name__))
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
        checked = self.check_duplicates(tab)
        if checked[0] is True:
            self.setCurrentIndex(checked[1])
        else:
            index = super().addTab(tab, os.path.split(tab.rootfield.name)[1])
            if tab.rootfield.description:
                self.setTabToolTip(index, tab.rootfield.description)
            self.setCurrentIndex(index)

    def add_rootfield(self, root):
        """Add new field root and create a ConfView object, by given rootfield."""
        tab = CompositeFieldView(root)
        tab.init_ui()
        self.addTab(tab)
        tab.show()

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
            self.removeTab(index)
            tab.close()

    def show_filename_status(self, index: int):
        """Add message to mainwindow statusbar."""
        if index != -1:
            tab = self.widget(index)
            mainwindow = get_main_window()
            mainwindow.statusbar.showMessage(tab.rootfield.name)
