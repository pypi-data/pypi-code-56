#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PySide2.QtCore import Slot
from PySide2.QtWidgets import QDialog, QLabel, QWidget

from prettyetc.baseui.ui import IndexableFieldUI
from prettyetc.etccore import (
    ArrayField, BoolField, DictField, FloatField, IndexableField, IntField,
    StringField)

from ..components.widgets.add import Ui_add_dialog
from ..inputs import GenericInputWrapper, field_to_widget
from ..utils import replace_widget, tr

__all__ = ("NewFieldDialog",)

FIELDTYPE_MAP = [
    StringField,
    IntField,
    FloatField,
    BoolField,
    ArrayField,
    DictField,
]


class NewFieldDialog(Ui_add_dialog, QDialog):
    """Create a new field into given IndexableFieldUI."""

    fielddata = None
    rejected = False

    def __init__(self,
                 parentfieldui: IndexableFieldUI,
                 parentwid: QWidget = None):
        super(NewFieldDialog, self).__init__(parent=parentwid)
        self.parentfieldui = parentfieldui
        self.setupUi(self)
        self.field_type.currentIndexChanged.connect(self.change_datatype_index)

    def accept(self):
        """Create the field and add it into the field and fieldui tree."""
        field = FIELDTYPE_MAP[self.field_type.currentIndex()](None)
        field.name = self.fieldname.text()

        if not isinstance(self.fielddata, QLabel):
            field.data = GenericInputWrapper.generate_wrapper(
                self.fielddata).value

        field.description = self.field_description.text()
        field.readonly = self.field_readonly.isChecked()

        fieldui = self.parentfieldui.create_child(field)
        fieldui.run(blocking=False)
        self.parentfieldui.add_field(fieldui, to_field=True)

        super().accept()

    def reject(self):
        """Set the dialog rejected flag to True."""
        super().reject()
        self.rejected = True

    @Slot(int)
    def change_datatype_index(self, index: int):
        """Change data widget."""
        fieldtype = FIELDTYPE_MAP[index]
        tempfield = fieldtype(None)
        wid = field_to_widget(tempfield, parent=self)

        if wid is None:
            if issubclass(fieldtype, IndexableField):
                wid = QLabel(
                    tr(self.objectName(),
                       "Collection field data can be setted in the tree view"))

        if wid is not None:
            self.fielddata = replace_widget(self.fielddata.parent().layout(),
                                            self.fielddata, wid)
