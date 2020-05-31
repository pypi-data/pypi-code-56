#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""All the field representations on view."""
import abc
from collections import OrderedDict
from functools import partial

from prettyetc.baseui.settings import SettingsManager
from prettyetc.baseui.ui.common import CommonComponent
from prettyetc.baseui.ui.field import RootFieldUI
from prettyetc.etccore.langlib import (BoolField, Field, FloatField,
                                       IndexableField, IntField, NameField,
                                       RootField, StringField)
from PySide2.QtWidgets import (QFrame, QPushButton, QSplitter, QTextEdit,
                               QTreeWidget, QTreeWidgetItem)

from .components.widgets.commonview import Ui_fieldview
from .components.widgets.details import Ui_details
from .field import (BaseFieldItem, BoolFieldItem, IterableFieldItem,
                    NameFieldItem, NumericFieldItem, StringFieldItem)
from .utils import tr

__all__ = ("CommonFieldView", "TreeFieldView", "SourceFieldView",
           "CompositeFieldView")


class CommonFieldViewMeta(abc.ABCMeta, type(QFrame)):
    """Join QFrame metaclass to CommonComponent metaclass."""


class DetailsView(QFrame, Ui_details):
    """
    Detail view of a field.
    It's intended to be used as right widget.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)


class CommonFieldView(
        QFrame, Ui_fieldview, CommonComponent, metaclass=CommonFieldViewMeta):
    """
    Basic configuration view.

    It supports multi view root.
    """

    def __init__(self, rootfield: RootField, *args, **kwargs):
        self.rootfield = rootfield
        self.root = None
        super().__init__(*args, **kwargs)
        self.settings = SettingsManager.factory(None)
        self.views = {}

    def change_view(self, viewkey: str, force: bool = False):
        """Change the view by given view key."""
        wid = self.views[viewkey]
        root = self.root

        if wid != root or force:
            self.rootLayout.replaceWidget(root, wid)
            wid.setSizePolicy(root.sizePolicy())
            root.setParent(None)
            wid.setParent(self)
            self.root = wid

    def init_ui(self):
        """Init common view."""
        self.setupUi(self)
        super().init_ui()

    def show(self):
        """Add views list to selector."""
        for label in self.views:
            button = QPushButton(self)
            button.setText(tr(self.objectName(), label))
            button.clicked.connect(partial(self.change_view, label))
            self.navbar.addWidget(button)

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


class TreeFieldView(RootFieldUI, CommonFieldView):
    """Display a Configuration file, using a list of indented fields."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.details_view = DetailsView()
        self.tree_view = QTreeWidget()

    def init_ui(self):
        """Init QTreeWidget and build tree UI."""
        super().init_ui()
        # widget configuration
        wid = QSplitter(parent=self)

        # tree configuration
        treewid = self.tree_view
        treewid.setParent(wid)
        wid.addWidget(treewid)

        # details configuration
        self.details_view.setParent(wid)
        wid.addWidget(self.details_view)

        self.views["Tree"] = wid

        # tree configuration
        treewid.setSortingEnabled(False)
        treewid.setHeaderHidden(True)
        treewid.setColumnCount(1)
        treewid.header().setSectionResizeMode(
            treewid.header().ResizeToContents)
        treewid.setStyleSheet("QTreeView::item {  padding-right:15px; }")
        treewid.itemClicked.connect(self.change_details)

        #  create tree
        tranformer = OrderedDict(
            [(IndexableField, IterableFieldItem), (NameField, NameFieldItem),
             (BoolField, BoolFieldItem), (IntField, NumericFieldItem),
             (FloatField,
              NumericFieldItem), (StringField,
                                  StringFieldItem), (Field, BaseFieldItem)])
        self.ui_builder(self.rootfield, transformer=tranformer)

        treewid.addTopLevelItems(self.tree.takeChildren())
        self.init_ui_all(exclude_root=True)

    def show(self):
        super().show()
        self.show_all(exclude_root=True)

    def close(self):
        self.close_all(exclude_root=True)
        super().close()

    def change_details(self, item: BaseFieldItem):
        """Change details informations with item informations."""
        field = item.field
        wid = self.details_view
        wid.fieldname.setText(str(field.name))
        if field.description in (None, ""):
            wid.field_description.setText(
                tr(self.objectName(), "No description avaiable."))
        else:
            wid.field_description.setText(str(field.description))

        # tree widget configuration
        show_object = self.settings.qtview.get("show objects", False)
        wid.field_attributes.clear()
        items = []
        if field.attributes is not None:
            for key, val in field.attributes.items():
                if isinstance(val, (str, int, float)) or show_object:
                    item = QTreeWidgetItem()
                    item.setText(0, str(key))
                    item.setText(1, str(val))
                    items.append(item)
        wid.field_attributes.addTopLevelItems(items)

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

    def init_ui(self):
        """Init QTreeWidget and build tree UI."""
        super().init_ui()
        # source configuration
        wid = QTextEdit()
        self.views["Source"] = wid

        try:
            wid.setText(self.rootfield.source)
        except ValueError:
            wid.setText("Sources are not avaiable.")

        wid.setReadOnly(True)


class CompositeFieldView(SourceFieldView, TreeFieldView):
    """Join all field views into 1 universal widget."""

    def show(self):
        """Show the preferred view depending of the rootfield type."""
        super().show()
        if isinstance(self.rootfield, RootField):
            viewkey = self.settings.qtview.get("rootfield default view",
                                               "Tree")
            self.change_view(viewkey)
        else:
            self.change_view("Source")
