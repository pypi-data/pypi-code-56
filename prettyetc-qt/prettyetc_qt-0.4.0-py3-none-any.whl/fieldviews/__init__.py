#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""All the field representations on view."""

import abc
import queue
from collections import OrderedDict
from functools import partial

from PySide2.QtCore import QObject, Signal, Slot
from PySide2.QtWidgets import (
    QApplication, QHBoxLayout, QPushButton, QSizePolicy, QSpacerItem,
    QSplitter, QTextEdit, QTreeWidget, QTreeWidgetItem, QVBoxLayout, QWidget)

from prettyetc.baseui.settings import SettingsManager
from prettyetc.baseui.ui import CommonComponent, RootFieldUI
from prettyetc.etccore.langlib import (
    BoolField, Field, FloatField, IndexableField, IntField, NameField,
    RootField, StringField)

from ..utils import get_main_window, replace_widget, tr
from .treeview import TreeView

__all__ = ("CommonFieldView", "TreeFieldView", "SourceFieldView",
           "CompositeFieldView")


class Signals(QObject):
    """All the internal signals used in this module."""


class CommonFieldViewMeta(abc.ABCMeta, type(QWidget)):
    """Join QWidget metaclass to CommonComponent metaclass."""


class CommonFieldView(CommonComponent, QWidget, metaclass=CommonFieldViewMeta):
    """
    Basic configuration view.

    It supports multi view root.
    """

    def __init__(self, rootfield: RootField, *args, **kwargs):
        self.rootfield = rootfield
        self.root = None
        self.rootLayout = None
        self.navbar = None

        super().__init__(*args, **kwargs)
        self.settings = SettingsManager.factory(None)
        self.views = {}
        self.signals = Signals()
        # self.signals.moveToThread(self.thread())

    def change_view(self, viewkey: str, force: bool = False):
        """Change the view by given view key."""
        wid = self.views[viewkey]
        root = self.root

        if wid != root or force:
            self.root = replace_widget(self.rootLayout, root, wid)
            self.root.setSizePolicy(root.sizePolicy())

    def init_ui(self, **_):
        """Init common view."""
        self.setObjectName("commonfieldview")
        self.rootLayout = QVBoxLayout(self)
        body = QWidget(self)
        self.navbar = QHBoxLayout(body)

        self.rootLayout.addWidget(body)

        self.root = QWidget(self)
        self.root.setObjectName("root")
        size_policy = QSizePolicy(QSizePolicy.Preferred,
                                  QSizePolicy.MinimumExpanding)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(
            self.root.sizePolicy().hasHeightForWidth())
        self.root.setSizePolicy(size_policy)

        self.rootLayout.addWidget(self.root)

        super().init_ui()

    def show(self):
        """Add views list to selector."""
        # remove all widgets in navbar
        for i in reversed(range(self.navbar.count())):
            self.navbar.itemAt(i).widget().setParent(None)

        for label in self.views:
            label = tr("commonfieldview", label)
            button = QPushButton(self)
            button.setText(tr(self.objectName(), label))
            button.clicked.connect(partial(self.change_view, label))
            self.navbar.addWidget(button)

        spacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.navbar.addItem(spacer)

    def find(self, text: str, datatype: str = "all") -> list:
        """Find all elements in rootfield."""
        if datatype == "all":
            found = self.rootfield.find_by_attr(
                force_string=True,
                name=text,
                data=text,
                description=text,
                multiple_fields=True,
                check_all=False)
        else:
            found = self.rootfield.find_by_attr(
                multiple_fields=True, force_string=True, **{datatype: text})

        return found

    def close(self):
        self.deleteLater()


class TreeFieldView(CommonFieldView):
    """Display a Configuration file, using a list of indented fields."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__field_view = TreeView(self.rootfield)
        self.views["Tree"] = self.__field_view
        self.__is_closed = False

    def init_ui(self, **kwargs):
        """Init QTreeWidget and build tree UI."""
        super().init_ui(**kwargs)

        self.__field_view.init_ui()

    def show(self):
        super().show()
        self.__field_view.show()

    def close(self):
        self.__is_closed = True
        self.__field_view.close()
        super().close()

    def find(self, *args, **kwargs) -> list:
        """Find and highlight every found FieldView."""
        found = super().find(*args, **kwargs)

        if self.root == self.views["Tree"]:
            # only in Tree mode
            for field in found:
                field.dispatch(True, "highlight")
        return found


class SourceFieldView(CommonFieldView):
    """Display a Configuration file, using its content."""

    def init_ui(self, **kwargs):
        """Init QTreeWidget and build tree UI."""
        wid = QTextEdit()
        wid.setObjectName("source_textedit")
        self.views["Source"] = wid
        super().init_ui(**kwargs)
        # source configuration

        try:
            wid.setText(self.rootfield.source)
        except ValueError:
            wid.setText(tr(
                wid.objectName(),
                "Source text is not available.",
            ))

        wid.setReadOnly(True)

    def reload(self, content: str = None):
        """Reload the source."""
        wid = self.views["Source"]
        del self.rootfield.source

        try:
            wid.setText(self.rootfield.source if content is None else content)

        except ValueError:
            wid.setText(tr(
                wid.objectName(),
                "Source text is not available.",
            ))

        else:
            if content is not None:
                self.rootfield.source = content


class CompositeFieldView(SourceFieldView, TreeFieldView):
    """Join all field views into 1 universal widget."""

    def show(self):
        """Show the preferred view depending of the rootfield type."""
        super().show()
        if isinstance(self.rootfield, RootField):
            viewkey = self.settings.qtview.get(
                "rootfield default view",
                "Tree",
            )
            self.change_view(viewkey)
        else:
            self.change_view("Source")
