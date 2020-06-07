#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Utilities to manage Qt input widgets in a abstract
and pythonic way.
"""

__all__ = ("GenericInputWrapper", "TempEditWrapper", "field_to_widget",
           "object_to_widget")
import sys

from PySide2.QtCore import QObject, Signal, Slot
from PySide2.QtWidgets import (
    QAbstractSpinBox, QCheckBox, QDialog, QDoubleSpinBox, QLineEdit,
    QPlainTextEdit, QSpinBox, QTreeWidgetItem, QWidget)

from prettyetc.baseui.ui import CommonComponent
from prettyetc.etccore import (
    BoolField, Field, FloatField, IntField, StringField)

from .components.widgets.input import Ui_inputdialog
from .utils import replace_widget

# from decimal import Decimal

MAXINT = 2**31 - 1


class QTextEditWrapper(QObject):
    """
    Wrap QTextEdit and QPlainTextEdit to support

    the GenericInputWrapper class.
    """
    editingFinished = Signal()

    def __init__(self, textedit):
        super().__init__()
        # self init
        self.widget = textedit
        self._old_focusout = textedit.focusOutEvent
        self.textChanged = textedit.textChanged

        # textedit init
        textedit.plainText = textedit.toPlainText
        textedit.focusOutEvent = self.focusout_patch

    def focusout_patch(self, event):
        """Monkey patch the text edit to propagate
        the editingFinished signal."""
        self.editingFinished.emit()
        self._old_focusout(event)

    def plainText(self):
        """Get text to text edit."""
        return self.widget.toPlainText()

    def setPlainText(self, text: str):
        """Set text to text edit."""
        return self.widget.setPlainText(text)

    def setDisabled(self, value: bool):
        """A shortcut for textedit.setDisabled."""
        self.widget.setDisabled(value)

    def deleteLater(self):
        """A shortcut for textedit.deleteLater."""
        self.widget.deleteLater()
        super().deleteLater()


class GenericInputWrapper(object):
    """
    Wrap a QWidget input to abstract its value management,
    indipendently from widget type,
    through through the value property.
    """
    __all__ = ("_widget", "field_setter", "on_edit_end", "on_update",
               "__weakref__")

    @classmethod
    def generate_wrapper(cls, widget: QWidget, **kwargs) -> object:
        """
        Try to generate a wrapper by given widget.

        Generation depends on widget type, and only few types are supported.
        """
        wrapper = None
        if isinstance(widget, QLineEdit):
            wrapper = cls(
                widget,
                "text",
                widget_edit_signal=widget.textEdited,
                widget_edit_end_signal=widget.editingFinished,
                **kwargs,
            )
        elif isinstance(widget, QPlainTextEdit):
            widget = QTextEditWrapper(widget)
            wrapper = cls(
                widget,
                "plainText",
                widget_edit_signal=widget.textChanged,
                widget_edit_end_signal=widget.editingFinished,
                **kwargs,
            )
        elif isinstance(widget, QAbstractSpinBox):
            wrapper = cls(
                widget,
                "value",
                widget_edit_signal=widget.valueChanged,
                widget_edit_end_signal=widget.editingFinished,
                **kwargs,
            )
        elif isinstance(widget, QCheckBox):
            widget.checked = widget.isChecked
            wrapper = cls(
                widget,
                "checked",
                widget_edit_signal=widget.toggled,
                widget_edit_end_signal=widget.toggled,
                **kwargs,
            )

        if wrapper is None:
            raise NotImplementedError("QWidget type {}  is unsupported.".format(
                type(widget).__name__))

        return wrapper

    def __init__(self,
                 widget: QWidget,
                 widget_propertyname: str,
                 widget_edit_signal: Signal = None,
                 widget_edit_end_signal: Signal = None,
                 field: Field = None,
                 field_property: str = None,
                 on_update: callable = lambda value: None,
                 on_edit_end: callable = lambda: None):

        super(GenericInputWrapper, self).__init__()

        self._widget = widget
        self.on_edit_end = on_edit_end
        self.on_update = on_update
        self.widget_propertyname = widget_propertyname

        # create field setter
        if field is not None and field_property is not None:
            self.field_setter = lambda value: setattr(field, field_property, value)
        else:
            self.field_setter = None

        # connect edit and edit end signals
        if widget_edit_signal is not None:
            widget_edit_signal.connect(self._on_update)

        if widget_edit_end_signal is not None:
            widget_edit_end_signal.connect(self._on_edit_end)

    @Slot(str)
    @Slot(int)
    @Slot(float)
    @Slot(bool)
    @Slot(object)
    def _on_update(self, value=None):
        """The _on_update method."""
        self.on_update(value)

    def _on_edit_end(self):
        """The _on_edit_end method."""
        if callable(self.field_setter):
            self.field_setter(self.value)
        self.on_edit_end()

    @property
    def widget(self) -> QWidget:
        """
        Get real widget instance, depending on internal widget's type.
        """
        if isinstance(self._widget, QWidget):
            return self._widget

        if isinstance(getattr(self._widget, "widget", None), QWidget):
            return self._widget.widget

        if isinstance(self._widget, QObject):
            # return first QWidget found in object children
            for child in self._widget.children:
                if isinstance(child, QWidget):
                    return child

        return None

    @property
    def value(self):
        """Widget value property."""
        return getattr(self._widget, self.widget_propertyname)()

    @value.setter
    def value(self, value):
        """The value property setter."""
        getattr(
            self._widget,
            "set{}{}".format(self.widget_propertyname[0].upper(),
                             self.widget_propertyname[1:]),
        )(value)

    @value.deleter
    def value(self):
        """The value property deleter."""
        if hasattr(self._widget, "clear"):
            self._widget.clear()
        else:
            try:
                self.value = None
            except Exception:  # pylint: disable=W0703
                pass

    def deleteLater(self):
        """An alias for widget.deleteLater."""
        self._widget.deleteLater()

    def setDisabled(self, value: bool):
        """An alias for widget.setDisabled."""
        self._widget.setDisabled(value)


class GenericDialogWrapper(GenericInputWrapper, Ui_inputdialog,
                           CommonComponent):
    """Wrap a QWidget input in a dialog."""

    __all__ = ("dialog", "__dict__")

    def __init__(self, *args, parent: QWidget = None, **kwargs):
        super().__init__(*args, **kwargs)
        self.dialog = QDialog(parent=parent)

    def _on_edit_end(self):
        if self.dialog.result() != QDialog.Rejected:
            super()._on_edit_end()
            self.dialog.accepted.disconnect(self._on_edit_end)
            self.dialog.accept()

    def init_ui(self):
        self.setupUi(self.dialog)
        replace_widget(self.layout, self.inputwid, self.widget)
        del self.inputwid

        # signals
        self.buttonbox.accepted.connect(self.dialog.accept)
        self.buttonbox.rejected.connect(self.dialog.reject)
        self.dialog.accepted.connect(self._on_edit_end)

    def show(self):
        """The show method."""
        self.dialog.exec_()
        self.dialog.show()

    def close(self):
        self.dialog.deleteLater()
        self.widget.deleteLater()


class TempEditWrapper(object):
    """
    A widget manager for a temp input in QTreeWidget.

    It sets the given widget at given index of given
    QTreeWidgetItem object.

    When editing is finished (on_edit_end),
    the widget value will be setted as text the item at index,
    and the widget will be removed from tree and destroyed.
    """
    __slots__ = ("treeitem", "index", "wid", "end", "_on_finish")

    def __init__(self,
                 treeitem: QTreeWidgetItem,
                 index: int,
                 widget: GenericInputWrapper,
                 on_finish: callable = None):

        super().__init__()
        self.treeitem = treeitem
        self.index = index
        self.wid = widget
        self.end = False
        self._on_finish = on_finish

        self.wid.on_edit_end = self.on_finish

        treeitem.treeWidget().setItemWidget(treeitem, index, self.wid.widget)

    def on_finish(self):
        """Apply changes after editing."""
        if callable(self._on_finish):
            self._on_finish()

        # cleanup
        self.treeitem.treeWidget().setItemWidget(
            self.treeitem,
            self.index,
            None,
        )

        self.treeitem.setText(self.index, self.wid.value)
        self.wid.deleteLater()
        self.end = True


def field_to_widget(field: Field, parent: QWidget = None) -> QWidget:
    """
    Convert given field's data to a QWidget.

    Usually, the created widget supports editing properly.

    If given field can't be converted, None will be returned
    """
    value = field.data
    retwid = None

    # create widget depending on value type
    if isinstance(field, StringField):
        retwid = QLineEdit(parent)
        retwid.setText(value)

    elif isinstance(field, IntField):

        retwid = QSpinBox(parent)
        retwid.setRange(-MAXINT, MAXINT)

        if value is not None:
            retwid.setValue(value)

    elif isinstance(field, FloatField):
        retwid = QDoubleSpinBox(parent)
        retwid.setRange(-sys.maxsize, sys.maxsize)

        retwid.setDecimals(14)
        # Decimal allows to not round floats and remove any extra 0 digits.
        # but does not allow to add extra digits when needed because the number of
        # decimal digits is fixed.
        # decimal = Decimal(str(value))
        # retwid.setDecimals(abs(decimal.as_tuple().exponent))
        if value is not None:
            retwid.setValue(value)

    elif isinstance(field, BoolField):
        retwid = QCheckBox(parent)
        if value is not None:
            retwid.setChecked(value)

        # patch QCheckBox to allow GenericDialogWrapper
        # to get checkbox's value
        retwid.checked = retwid.isChecked

    return retwid


def object_to_widget(obj: object, parent: QWidget = None) -> QWidget:
    """
    Convert given object to a QWidget.

    Usually, the created widget supports editing properly.

    If given object can't be converted, None will be returned.
    """
    retwid = None

    # create widget depending on value type
    if isinstance(obj, str):
        retwid = QLineEdit(parent)
        retwid.setText(obj)

    elif isinstance(obj, bool):
        retwid = QCheckBox(parent)
        retwid.setChecked(obj)
        retwid.checked = retwid.isChecked

    elif isinstance(obj, int):
        retwid = QSpinBox(parent)
        retwid.setValue(obj)

    elif isinstance(obj, float):
        retwid = QDoubleSpinBox(parent)

        retwid.setDecimals(14)
        # Decimal allows to not round floats and remove any extra 0 digits.
        # but does not allow to add extra digits when needed because the number of
        # decimal digits is fixed.
        # decimal = Decimal(str(value))
        # retwid.setDecimals(abs(decimal.as_tuple().exponent))

        retwid.setValue(obj)

    return retwid


# def widget_to_object(widget: QWidget) -> object:
#     """
#     Convert given widget to a python object.
#
#     This method is useful for handling different getter methods
#     that Qt widgets have.
#     """
#     value = None
#     if isinstance(widget, QLineEdit):
#         value = widget.text()
#
#     elif isinstance(widget, QAbstractSpinBox):
#         value = widget.value()
#
#     elif isinstance(widget, QCheckBox):
#         value = widget.isChecked()
#
#     else:
#         value = None
#
#     return value
