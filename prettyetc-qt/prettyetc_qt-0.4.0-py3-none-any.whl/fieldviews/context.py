#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Basic context menu for field views."""

import abc
from functools import partial

from PySide2.QtCore import QPoint, Slot
from PySide2.QtWidgets import (
    QApplication, QLineEdit, QMenu, QMessageBox, QPlainTextEdit, QWidget)

from prettyetc.baseui.ui import CommonComponent
from prettyetc.etccore import IndexableField

from ..inputs import GenericDialogWrapper, field_to_widget
from ..utils import tr
from .common import NewFieldDialog

__all__ = ("FieldMenu", "TreeItemMenu")


# metaclasses
class BaseFieldMenuMeta(abc.ABCMeta, type(QMenu)):
    """Join QMenu metaclass to CommonComponent metaclass."""


class FieldMenu(CommonComponent, QMenu, metaclass=BaseFieldMenuMeta):
    """A view-indipendently context menu for editing fields."""

    loggername = "qtui.fieldviews.context"

    attributes = ("name", "data", "description", "readonly")

    def __init__(self, parent: QWidget = None):
        self.field = None
        super().__init__(parent=parent)
        self.setObjectName("field_context")

        self.default_actions = []

    def init_ui(self):
        """
        Create the common actions and bind them.

        All of actions added here will be always shown.
        """
        # set actions
        actions = [
            self.addAction(tr("field_context", "Set Name")),
            self.addAction(tr("field_context", "Set Data")),
            self.addAction(tr("field_context", "Set Description")),
            # self.addAction(tr("field_context", "set attributes")),
            self.addAction(tr("field_context", "toggle readonly")),
        ]
        self.default_actions.extend(actions)

        for action, attr in zip(actions, self.attributes):
            if attr == "readonly":
                action.triggered.connect(self.toggle_readonly)
            else:
                action.triggered.connect(
                    partial(self.action_wrapper, attr, action.text()))

        self.default_actions.extend([
            self.addSeparator(),
            self.addAction(tr("field_context", "Delete"))
        ])

    def show(self, point: QPoint):
        self.exec_(point)

    def close(self):
        """Clear menu state."""
        self.field = None

        # disconnect all action signals
        for action in self.actions():
            try:
                action.triggered.disconnect()
            except RuntimeError:
                pass

        # clear actions
        self.clear()

        # recreate actions
        self.default_actions = []
        QApplication.processEvents()
        self.init_ui()
        # self.actions.clear()
        self.hide()

    # slots
    @Slot(QPoint)
    def on_context_menu(self, point: QPoint):
        """Show the context menu if possible."""
        if self.field is not None:
            field = self.field

            # add "Add field" action if field is an IndexableField
            if isinstance(field, IndexableField):
                actions = (
                    self.addSeparator(),
                    self.addAction(tr("field_context", "Add field")),
                )
                actions[1].triggered.connect(self.add_field)

            self.show(point)
            self.close()

    def add_field(self):
        """
        Open the New field dialog.

        An implementation is required
        """
        raise NotImplementedError()

    def toggle_readonly(self):
        """Invert field readonly."""
        self.field.readonly = not self.field.readonly

    def action_wrapper(self,
                       attr: str,
                       window_title: str = None,
                       _: bool = False):
        """Show an input dialog."""
        if self.field.readonly:
            QMessageBox.warning(
                self,
                tr("field_context", "Field is readonly"),
                tr("field_context",
                   "Cannot edit this field because it is readonly."),
            )
        else:
            field = self.field
            wid = None
            if attr == "name":
                wid = QLineEdit(field.name)
            elif attr == "data" and not isinstance(field, IndexableField):
                wid = field_to_widget(field)
            elif attr == "description":
                wid = QPlainTextEdit(field.description)

            # widget configuration
            # text = action.text()
            if window_title is not None:
                wid.setWindowTitle(window_title)

            # # parameter configuration
            # if text.lower().startswith("set "):
            #     text = text[4:] + ":"

            wid = GenericDialogWrapper.generate_wrapper(
                wid, field=field, field_property=attr)
            wid.run()


class TreeItemMenu(FieldMenu):

    fieldui = None

    def init_ui(self):
        super().init_ui()
        self.default_actions[5].triggered.connect(self.remove_field)

    def on_context_menu(self, point: QPoint):
        """Show the context menu if possible."""
        treeitem = self.parent().itemAt(point)
        if treeitem is not None:
            self.fieldui = treeitem
            self.field = treeitem.field

        super().on_context_menu(self.parent().mapToGlobal(point))

    def add_field(self):

        if self.fieldui is not None:
            add_dialog = NewFieldDialog(self.fieldui, parentwid=self.parent())
            add_dialog.show()
            add_dialog.exec_()

    def remove_field(self):
        """Remove the field, if setted."""
        if self.fieldui is None:
            # I hope that this message box never show
            QMessageBox.error(
                self,
                tr("field_context", "Error"),
                tr("field_context", "Can't remove the field"),
            )
        else:
            parent = self.fieldui.parent()
            if parent is None:
                parent = self.fieldui.treeWidget()

            parent.remove_field(self.fieldui, from_field=True)

    def close(self):
        self.fieldui = None
        super().close()
