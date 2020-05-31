#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Show and manage all kind of fields."""

import abc

from prettyetc.baseui import (BaseFieldUI, CommonComponent, IndexableFieldUI,
                              SettingsManager)
from prettyetc.etccore.langlib import Field, FloatField
from PySide2.QtCore import Qt
from PySide2.QtWidgets import (QCheckBox, QDoubleSpinBox, QSpinBox,
                               QTreeWidgetItem, QWidget)

from .components.widgets.field import Ui_field

__all__ = ("BaseFieldItem", "StringFieldItem", "NumericFieldItem",
           "BoolFieldItem", "NameFieldItem", "IterableFieldItem")


class BaseFieldItemMeta(abc.ABCMeta, type(QTreeWidgetItem)):
    """Join QTreeWidgetItem metaclass to BaseFieldUI metaclass."""


class FieldWidgetMeta(abc.ABCMeta, type(QWidget)):
    """Join QWidget metaclass to CommonComponent metaclass."""


class FieldWidget(
        QWidget, Ui_field, CommonComponent, metaclass=FieldWidgetMeta):
    """Field main widget."""

    def __init__(self, *args, allow_edit=False, **kwargs):
        self.settings = SettingsManager.factory(None)
        self.allow_edit = allow_edit
        super().__init__(*args, **kwargs)
        self.setVisible(False)
        self._orig_stylesheet = None

    def init_ui(self):
        super().init_ui()
        self.setupUi(self)

        self._orig_stylesheet = self.styleSheet()

        if not self.allow_edit:
            self.layout.removeWidget(self.minus)
            self.minus.setParent(None)
            self.layout.removeWidget(self.plus)
            self.plus.setParent(None)

    def show(self):
        super().show()
        self.setVisible(True)

    @property
    def highlight(self) -> bool:
        """Toggle widget highlight."""
        return self.styleSheet() != self._orig_stylesheet

    @highlight.setter
    def highlight(self, value: bool):
        """The highlight property setter."""
        if value:
            lightness = self.palette().color(
                self.backgroundRole()).lightnessF()
            if self.settings.qtappearance.get("selected color"):
                bg_color = self.settings.qtappearance.get("selected color")
            elif lightness > 0.5:
                bg_color = "#2962ff"
            else:
                # bg_color = "#e65100" # orange
                bg_color = "#2962ff" # blue

            self.setStyleSheet(self._orig_stylesheet +
                               "\nbackground-color: {};".format(bg_color))

        else:
            self.setStyleSheet(self._orig_stylesheet)
        # print("styleSheet", self.styleSheet(), "value", value)


class BaseFieldItem(BaseFieldUI, QTreeWidgetItem, metaclass=BaseFieldItemMeta):
    """
    Display a string field, using text field (QLineEdit) and manage interaction.

    This base class represent the base for fields views.
    """

    def __init__(self, field: Field):
        # widgets init
        self.wid = FieldWidget()

        super().__init__(field)
        self.setHidden(True)

    def init_ui(self):
        """Init QTreeWidgetItem and create field widgets."""
        super().init_ui()
        self.wid.init_ui()
        self.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEditable
                      | Qt.ItemIsDragEnabled | Qt.ItemIsDropEnabled
                      | Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
        treewidget = self.treeWidget()
        treewidget.setItemWidget(self, 0, self.wid)

        # self.setText(0, "")
        # self.setText(1, "")
        # self.namewid = treewidget.itemWidget(self, 0)
        # self.datawid = treewidget.itemWidget(self, 1)
        # self.namewid.setText(0, "")

        # cells init

        # self.plus = QToolButton(treewidget)
        # self.plus.setText("+")
        # self.minus = QToolButton(treewidget)
        # self.minus.setText("-")
        # item widget init

        # treewidget.setItemWidget(self, 2, self.plus)
        # treewidget.setItemWidget(self, 3, self.minus)
        # treewidget.setItemWidget(self, 4, QWidget())
        treewidget.setItemWidget(self, 1, QWidget())

        # field listener
        self.field.listener = self.on_field_event

    def show(self):
        """Enable the item."""
        super().show()
        self.wid.show()
        self.setHidden(False)

        self.setExpanded(True)

        self.name = self.name
        self.data2 = self.data2
        self.description = self.description
        self.attributes = self.attributes

    def close(self):
        """Destroy the item."""
        super().close()
        self.setDisabled(False)

    def on_field_event(self, value, valuetype):
        """Catch highlight event for highlighting field."""
        if valuetype == "highlight":
            self.wid.highlight = value

    # field properties
    @property
    def name(self):
        """
        Field name.

        Assing to it will assing both to the name widget and the Field.name attribute.
        """
        return self.field.name

    @name.setter
    def name(self, value):
        self.field.name = value
        if value is None:
            value = ""
        self.wid.name.setText(str(value))

    @property
    def data2(self):
        """
        Field data.

        Assing to it will assing both to the data widget and the Field.data attribute.
        """
        return self.field.data

    @data2.setter
    def data2(self, value):
        self.field.data = value
        # self.datawid.setText(str(value))
        self.wid.data.setVisible(bool(value))
        self.wid.data.setText(str(value))

    @property
    def description(self):
        """
        Field description.

        Assing to it will assing both to the name widget and the Field.description attribute.
        """
        return self.field.description

    @description.setter
    def description(self, value):
        self.field.description = value
        # self.descriptionwid.setText(value)

    @property
    def attributes(self):
        """
        Field attributes.

        Assinging to it will assing both to the attributes widget
        and the Field.attributes attribute.
        """
        return self.field.attributes

    @attributes.setter
    def attributes(self, value):
        self.field.attributes = value
        # self.attributeswid.setText(value)

    @property
    def datawid(self):
        """Field data widget."""
        return self.wid.data

    @datawid.setter
    def datawid(self, value):
        self.wid.datalayout.replaceWidget(self.wid.data, value)
        self.wid.data.setParent(None)
        self.wid.data = value
        # self.treeWidget().setItemWidget(self, 2, value)


class StringFieldItem(BaseFieldItem):
    """Display a string field, using QTextEdit."""


class NumericFieldItem(BaseFieldItem):
    """Display a numeric field, integer or float, using spinbox."""

    def init_ui(self, use_super=True):
        if use_super:
            super().init_ui()

        if isinstance(self.field, FloatField):
            self.datawid = QDoubleSpinBox()
        else:
            self.datawid = QSpinBox()

    @property
    def data2(self):
        """
        Field data.

        Assing to it will assing both to the data widget and the Field.data attribute.
        """
        return self.field.data

    @data2.setter
    def data2(self, value):
        old_data = self.data2
        self.field.data = value
        if type(value) != type(old_data):  # pylint: disable=C0123
            self.init_ui(use_super=False)
        self.datawid.setValue(value)


class BoolFieldItem(BaseFieldItem):
    """Display a boolean field, using checkbox."""

    def init_ui(self):
        super().init_ui()
        self.datawid = QCheckBox()

    @property
    def data2(self):
        """
        Field data.

        Assing to it will assing both to the data widget and the Field.data attribute.
        """
        return self.field.data

    @data2.setter
    def data2(self, value):
        self.field.data = value
        self.datawid.setChecked(bool(value))


class NameFieldItem(BaseFieldItem):
    """Display a field that haven't data."""

    def init_ui(self):
        """Disable data widget."""
        super().init_ui()
        self.datawid = QWidget()

    @property
    def data2(self):
        """
        Field data.

        Assing to it will assing both to the data widget and the Field.data attribute.
        """
        return self.field.data

    @data2.setter
    def data2(self, value):
        self.field.data = value


class IterableFieldItem(NameFieldItem, IndexableFieldUI):
    """
    Display an iterable field, with name and description only.

    Field data is represented as list of children using a tree
    structure.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.addChildren(self.children)

    def add_field(self, node: BaseFieldItem):
        super().add_field(node)
        self.addChild(node)
