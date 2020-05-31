#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Show and manage all kind of fields."""

import abc

from PySide2.QtCore import Qt
from PySide2.QtWidgets import (QCheckBox, QDoubleSpinBox, QSpinBox,
                               QToolButton, QTreeWidgetItem, QWidget)

from prettyetc.etccore.langlib import Field, FloatField, IntField

__all__ = ("BaseFieldItem", "StringFieldItem", "NumericFieldItem",
           "BoolFieldItem", "NoDataFieldItem", "IterableFieldItem")


class BaseFieldItem(QTreeWidgetItem):
    """
    Display a string field, using textarea and manage interaction.

    This base class represent the base for fields views. Initialization
    and updating of field is done in the update_field method, doing
    properly type controls. See update_field method documentation for
    more information.

    """
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def field_dispatch(self, value, valuetype="data"):
        """
        Handle single changes to.

        Usually this method is not called by hand, but it is
        automatically called by field event.
        .. seealso::
            Class :py:class:confparser.langlib.Field
            For more information about field event system.

        """

    @abc.abstractmethod
    def update_field(self, field):
        """
        Update widget by new field data.

        It sets data, name and description to the widget. It must be
        overriden by subclasses for handling different field types.
        Usually this method is not called by hand, but it is
        automatically called on setting the field attribute of this
        object.
        .. warning::
            This method DO NOT set the field attribute.

        """

    def __init__(self,
                 parent=None,
                 field=None,
                 treeview=None,
                 datatip="tooltip"):
        super().__init__(parent if parent is not None else treeview)

        # hidden init
        self._field = None
        self._namewid = None
        self._datawid = None
        # cells init
        treewidget = self.treeWidget()
        self.setText(0, "")
        self.setText(1, "")
        self.plus = QToolButton(treewidget)
        self.plus.setText("+")
        self.minus = QToolButton(treewidget)
        self.minus.setText("-")
        # item widget init
        self.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEditable
                      | Qt.ItemIsDragEnabled | Qt.ItemIsDropEnabled
                      | Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)

        treewidget.setItemWidget(self, 2, self.plus)
        treewidget.setItemWidget(self, 3, self.minus)
        treewidget.setItemWidget(self, 4, QWidget())
        # attributes init
        self.datatip = datatip
        self.field = field

    @property
    def fieldname(self):
        """Get the text name"""
        if self._namewid is None:
            return self.text(0)
        return self._namewid

    def change_datawidget(self, wid):
        """Change data widget with given widget."""
        self.treeWidget().setItemWidget(self, 1, wid)
        self._datawid = wid

    def setDataTip(self, tip, column=1):
        """Set description view."""
        if self.datatip == "tooltip":
            self.setToolTip(column, tip)
        #     try:
        #         widget.setToolTip(tip)
        #     except AttributeError:
        #         # data has not attribute setToolTip
        #         super().setDataTip(tip)
        # elif self.datatip == "datatip":
        #     super().setDataTip(tip)

    # useless
    # def parent_count(self):
    #     """Count parent children."""
    #     count = 0
    #     parent = self.parent()
    #     while parent is not None:
    #         count += 1
    #         parent = parent.parent()
    #     return count

    @property
    def field(self):
        """Get the field."""
        return self._field

    @field.setter
    def field(self, value):
        """Set the field and move update_field event from old to new field."""
        if value is not None:
            if isinstance(self._field, Field) and self._field != value:
                # move field event
                oldfield = self._field
                oldfield.listener.clear()
            value.listener = self.field_dispatch
            self.update_field(value)
        self._field = value

    @fieldname.setter
    def fieldname(self, val):
        """Set the text name."""
        if self._namewid is None:
            self.setText(0, val)
        else:
            self._namewid = val

    @property
    def fielddata(self):
        """Get the text data"""
        if self._datawid is None:
            return self.text(1)
        return self._datawid

    @fielddata.setter
    def fielddata(self, val):
        """Set the text data."""
        if self._datawid is None:
            self.setText(1, val)
        else:
            self._datawid = val


class StringFieldItem(BaseFieldItem):
    """Display a string field, using textedit."""

    def field_dispatch(self, value, valuetype="data"):
        if valuetype == "data":
            text = str(value).strip("\"")
            self.fielddata = text
        elif valuetype == "name":
            self.fieldname = value
        elif valuetype == "description":
            self.setDataTip(value)

    def update_field(self, field):
        self.field_dispatch(field.name, "name")
        self.field_dispatch(field.data, "data")
        self.field_dispatch(field.description, "description")

        # Managed by QTreeWidget
        # @property
        # def iden(self):
        #     """The identation property getter."""
        #     self.identation.width()
        #
        # @iden.setter
        # def iden(self, value):
        #     """The identation property setter."""
        #     self.identation.setFixedWidth(value)


class NumericFieldItem(BaseFieldItem):
    """Display a numeric field, integer or float, using spinbox."""

    def field_dispatch(self, value, valuetype="data"):
        if valuetype == "data":
            self.fielddata.setValue(value)
        elif valuetype == "name":
            self.fieldname = value
        elif valuetype == "description":
            self.setDataTip(value)

    def update_field(self, field):
        if isinstance(field, IntField):
            fielddata = QSpinBox()
        elif isinstance(field, FloatField):
            fielddata = QDoubleSpinBox()
        else:
            raise TypeError("Invalid field type {}.".format(
                type(field).__name__))
        self.change_datawidget(fielddata)
        self.field_dispatch(field.name, "name")
        self.field_dispatch(field.data, "data")
        self.field_dispatch(field.description, "description")


class BoolFieldItem(BaseFieldItem):
    """Display a boolean field, using checkbox."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        fielddata = QCheckBox()
        self.change_datawidget(fielddata)

    def field_dispatch(self, value, valuetype="data"):
        if valuetype == "data":
            self.fielddata.setChecked(bool(value))
        elif valuetype == "name":
            self.fieldname = value
        elif valuetype == "description":
            self.setDataTip(value)

    def update_field(self, field):
        self.field_dispatch(field.name, "name")
        self.field_dispatch(field.data, "data")
        self.field_dispatch(field.description, "description")


class NoDataFieldItem(BaseFieldItem):
    """
    Display a field, that have name and description only.

    If datatip is tooltip, tooltip is placed on name instead of on data.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.change_datawidget(QWidget())

    def setDataTip(self, tip, column=0):
        """Add tip to name instead of data."""
        super().setDataTip(tip, 0)

    def field_dispatch(self, value, valuetype="data"):
        # data valuetype is unsupported at the moment
        if valuetype == "name":
            self.fieldname = value
        elif valuetype == "description":
            # self.fieldname.setToolTip(value)
            pass

    def update_field(self, field):
        self.field_dispatch(field.name, "name")
        self.field_dispatch(field.description, "description")


class IterableFieldItem(NoDataFieldItem):
    """
    Display an iterable field, with name and description only.

    Field data is represented as list of children using a tree
    structure.
    """
