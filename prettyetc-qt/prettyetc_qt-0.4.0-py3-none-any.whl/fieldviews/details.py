#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import abc

from PySide2.QtCore import Slot
from PySide2.QtWidgets import QHeaderView, QLabel, QTreeWidgetItem, QWidget

from prettyetc.baseui.ui import CommonComponent
from prettyetc.etccore import Field

from ..components.widgets.details import Ui_FieldDetails
from ..inputs import (
    GenericInputWrapper, TempEditWrapper, field_to_widget, object_to_widget)
from ..utils import replace_widget, tr

__all__ = ("FieldDetailsView",)


class BaseWidgetMeta(abc.ABCMeta, type(QWidget)):
    """Join QWidget metaclass to CommonComponent metaclass."""


class FieldDetailsView(
        CommonComponent, Ui_FieldDetails, QWidget, metaclass=BaseWidgetMeta):
    """A generic field details view that allows to edit field's attrs."""

    def __init__(self, *args, parent: QWidget = None, **kwargs):
        self._current_field = None
        self._current_edit = None

        super().__init__(parent=parent)
        self.setVisible(False)

        # field widget definitons
        self.fieldname = None
        self.fielddata = None
        self.field_description = None
        self.field_attributes = None
        self.field_readonly = None

    def field_event(self, value, valuetype: str = 'data'):
        """Update widgets on field update."""

        if valuetype == "name":
            self.fieldname.value = value

        elif valuetype == "data" and isinstance(self.fielddata,
                                                GenericInputWrapper):
            self.fielddata.value = value

        elif valuetype == "description":
            self.field_description.value = value

        elif valuetype == "attributes":
            self.field_attributes.clear()
            for key, val in self.current_field.attrs.items():
                treeitem = QTreeWidgetItem([str(key), str(val)])
                treeitem.attrkey = key
                self.field_attributes.addTopLevelItem(treeitem)

    def init_ui(self):
        self.setupUi(self)

        # wrap all the field inputs into a GenericInputWrapper
        self.fieldname = GenericInputWrapper.generate_wrapper(self.fieldname)
        self.fielddata = GenericInputWrapper.generate_wrapper(self.fielddata)
        self.field_description = GenericInputWrapper.generate_wrapper(
            self.field_description)
        # self.field_attributes = self.field_attributes

        self.field_readonly = GenericInputWrapper.generate_wrapper(
            self.field_readonly)

        # widget extra configuration
        self.field_attributes.header().setSectionResizeMode(QHeaderView.Stretch)

    def show(self):
        self.field_attributes.itemDoubleClicked.connect(
            self.on_attibute_double_click)

        self.current_field = None
        self.setVisible(True)

        super().show()

    def close(self):
        self.deleteLater()

    @property
    def current_field(self) -> Field:
        """Current displayed field."""
        return self._current_field

    @current_field.setter
    def current_field(self, field: Field):
        """The current_field property setter."""
        if self._current_field is not None:
            self._current_field.listener.remove(self.field_event)

        self._current_field = field

        if field is None:
            # disable all inputs, including readonly
            self.toggle_disable(True)
            self.field_readonly.setDisabled(True)
        else:
            # readonly enable and executing
            self.field_readonly.setDisabled(False)
            self.toggle_disable(field.readonly)

            # create data widget
            self.fielddata = self._change_widget(self.fielddata)

            # set widget properties

            self.fieldname.field_setter = lambda value: setattr(field, "name", value)
            self.fielddata.field_setter = lambda value: setattr(field, "data", value)
            self.field_description.field_setter = lambda value: setattr(field, "description", value)
            self.field_readonly.field_setter = lambda value: setattr(field, "readonly", value)
            self.field_readonly.on_update = self.toggle_disable
            # self.field_attributes.field_setter = lambda value: setattr(field, "attributes", value)
            self.field_readonly.value = field.readonly

            # set field properties
            self.current_field.listener = self.field_event

            # dispatch values
            field.dispatch(field.name, "name")
            field.dispatch(field.data, "data")
            field.dispatch(field.description, "description")
            field.dispatch(field.attrs, "attributes")

    @Slot(bool)
    def toggle_disable(self, disabled: bool):
        """Disable all data widgets or not depending on readonly value (disabled)."""
        self.fieldname.setDisabled(disabled)
        self.fielddata.setDisabled(disabled)
        self.field_description.setDisabled(disabled)
        self.field_attributes.setDisabled(disabled)

    @Slot(QTreeWidgetItem, int)
    def on_attibute_double_click(self, item: QTreeWidgetItem, index: int):
        """Create a temp edit for item columns."""
        if self._current_edit is not None and self._current_edit.end:
            self._current_edit = None

        if self._current_edit is None:
            if index == 0:
                val = item.attrkey
            elif index == 1:
                val = self.current_attrs[item.attrkey]

            wid = GenericInputWrapper.generate_wrapper(
                object_to_widget(val, parent=self))

            self._current_edit = TempEditWrapper(
                item,
                index,
                wid,
                on_finish=self.on_attribute_edit_end,
            )

    def on_attribute_edit_end(self):
        """Set temp edit value to attribute key or value depending on index."""
        if self._current_edit is not None:
            tempedit = self._current_edit
            attrs = self.current_field.attrs
            value = tempedit.wid.value
            if tempedit.index == 0:
                attrs[value] = attrs[tempedit.treeitem.attrkey]
                del attrs[tempedit.treeitem.attrkey]
                tempedit.treeitem.attrkey = value

            elif tempedit.index == 1:
                attrs[tempedit.treeitem.attrkey] = value

    def _change_widget(self, widget):
        """Change given widget by field data."""
        if isinstance(widget, GenericInputWrapper):

            old_widget = widget.widget
        else:
            old_widget = widget

        old_layout = old_widget.parent().layout()
        new_wid = field_to_widget(self.current_field, self)
        if new_wid is None:
            wid_inst = new_wid = QLabel(
                tr(self.objectName(),
                   "Can't edit data here, use the tree view instead"))
            wid_inst.setWordWrap(True)
        else:
            new_wid = GenericInputWrapper.generate_wrapper(new_wid)
            wid_inst = new_wid.widget

        replace_widget(old_layout, old_widget, wid_inst)

        return new_wid
