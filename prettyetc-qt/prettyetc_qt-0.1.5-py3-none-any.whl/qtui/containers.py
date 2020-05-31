#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""All code containers."""
import os.path

from PySide2.QtWidgets import QTabWidget, QTreeWidget

from prettyetc.etccore.langlib import (BoolField, Field, FloatField, IndexableField,
                             IntField, NameField, RootField, StringField)

from .field import (BoolFieldItem, IterableFieldItem, NoDataFieldItem,
                    NumericFieldItem, StringFieldItem)

__all__ = ("ConfTab", "ConfView")


class ConfTab(QTabWidget):
    """Display and manage the main view of configs (by tab widget)."""

    rootConfs = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tabCloseRequested.connect(self.on_tab_close)

    def __add__(self, root):
        """A shortcut for the add_* method."""
        if isinstance(root, ConfView):
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
        tab = ConfView(root)
        self.addTab(tab)

    def check_duplicates(self, tab):
        """
        Check if tabname is already in tabs.

        Return True if a tab has the same name.
        Return a list of tuple that contains the different tab and the common path head.
        TODO: finish that method
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

    def on_tab_close(self, index, *_):
        """Called when tab is closing."""
        if index != -1:
            self.removeTab(index)


class ConfView(QTreeWidget):
    """Display a Configuration file, using a list of indented fields."""

    def __init__(self, root, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # tree configuration
        self.setSortingEnabled(False)
        self.setAnimated(False)
        self.setHeaderHidden(True)
        self.setColumnCount(5)
        self.header().setSectionResizeMode(self.header().ResizeToContents)
        self.setStyleSheet("QTreeView::item {  padding-right:15px; }")

        fieldviews = self._create_tree(root)
        self.insertTopLevelItems(0, fieldviews)
        self.rootfield = root

    def _create_tree(self, root, parent=None):
        """Recursive method to create field tree view."""
        fieldwiews = []
        for field in root:
            if not isinstance(field, Field):
                # suppose root is a dict like field and field is the key
                field = root[field]
            if isinstance(field, NameField):
                fieldview = NoDataFieldItem(
                    field=field, treeview=self, parent=parent)
            elif isinstance(field, StringField):
                fieldview = StringFieldItem(
                    field=field, treeview=self, parent=parent)
            elif isinstance(field, (IntField, FloatField)):
                fieldview = NumericFieldItem(
                    field=field, treeview=self, parent=parent)
            elif isinstance(field, BoolField):
                fieldview = BoolFieldItem(
                    field=field, treeview=self, parent=parent)
            elif isinstance(field, IndexableField):
                fieldview = IterableFieldItem(
                    field=field, treeview=self, parent=parent)
                children_fieldview = self._create_tree(field, fieldview)
                fieldview.insertChildren(0, children_fieldview)
            else:
                raise NotImplementedError(
                    "Field typed {} is not implemented yet.".format(
                        type(field).__name__))
            fieldwiews.append(fieldview)
        return fieldwiews
