#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import abc
import gc
from collections import OrderedDict
from multiprocessing.pool import ThreadPool
from threading import Thread

from PySide2.QtCore import Qt, QThreadPool, Slot
from PySide2.QtGui import QKeySequence
from PySide2.QtWidgets import (
    QFrame, QLineEdit, QMessageBox, QShortcut, QTreeWidget, QTreeWidgetItem,
    QWidget)

from prettyetc.baseui import SettingsManager
from prettyetc.baseui.ui import (
    BaseFieldUI, CommonComponent, IndexableFieldUI, RootFieldUI)
from prettyetc.etccore import Field, IndexableField, RootField

from ..components.widgets.treeview import Ui_TreeView
from ..inputs import GenericInputWrapper, TempEditWrapper, field_to_widget
from ..utils import RunnableWrapper, get_main_window, tr, tranfer_properties
from .common import NewFieldDialog
from .context import TreeItemMenu
from .details import FieldDetailsView

__all__ = ("BaseFieldItem", "IterableFieldItem", "FieldTreeWidget", "TreeView")


# metaclasses
class BaseFieldItemMeta(abc.ABCMeta, type(QTreeWidgetItem)):
    """Join QTreeWidgetItem metaclass to BaseFieldUI metaclass."""


class BaseTreeWidgetMeta(abc.ABCMeta, type(QTreeWidget)):
    """Join QTreeWidget metaclass to BaseFieldUI metaclass."""


class BaseFrameMeta(abc.ABCMeta, type(QFrame)):
    """Join QFrame metaclass to CommonComponent metaclass."""


class BaseFieldItem(BaseFieldUI, QTreeWidgetItem, metaclass=BaseFieldItemMeta):
    """
    Display a string field, using text field and manage field events.

    This base class represent the base for fields items.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.field.listener = self.field_event
        # self.setFlags(self.flags() | Qt.ItemIsDragEnabled)

    def __eq__(self, other):
        return id(self) == id(other)

    def field_event(self, value, valuetype: str = 'data'):
        """Update cells on field update."""
        if valuetype == "data":
            self.data2 = value

        elif valuetype == "highlight":
            self.setSelected(value)
            if value is True:
                parent = self
                while parent is not None:
                    parent.setExpanded(True)
                    parent = parent.parent()

        elif hasattr(self, valuetype):
            setattr(self, valuetype, value)

    # def init_ui(self):
    #     self.field.listener = self.field_event
    #     self.setText(0, "")
    #     self.setText(1, "")

    def show(self):
        self.field.dispatch(self.field.name, "name")
        self.field.dispatch(self.field.data, "data")
        self.field.dispatch(self.field.description, "description")

    def close(self):
        self.field.listener.remove(self.field_event)
        self.setHidden(True)

    @property
    def name(self):
        """
        Field name.

        Assing to it will assing both to the name widget and the Field.name attribute.
        """
        return self.text(0)

    @name.setter
    def name(self, value: str):
        if self.name != value:
            self.setText(0, str(value))

    @property
    def data2(self):
        """
        Field data.

        Assing to it will assing both to the data widget and the Field.data attribute.
        """
        return self.text(1)

    @data2.setter
    def data2(self, value):
        if self.data2 != value:
            self.setText(1, str(value))

    @property
    def description(self):
        """
        Field description.

        Assing to it will assing both to the description widget and the Field.description attribute.
        """
        return self.toolTip(0)

    @description.setter
    def description(self, value: str):
        if self.description != value:
            self.setToolTip(0, value)


class IterableFieldItem(BaseFieldItem, IndexableFieldUI):
    """
    Display an iterable field, only with the name.

    Field data is represented as list of children using a tree
    structure.
    """

    @classmethod
    def create_child(cls, field: Field, transformer: dict = None):
        if transformer is None:
            transformer = _ui_tranformer

        return super().create_child(field, transformer)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.addChildren(self.children)
        # self.setFlags(self.flags() | Qt.ItemIsDropEnabled)

    # def init_ui(self):
    #     self.setText(0, "")

    def add_field(self, node: BaseFieldItem, to_field: bool = False):
        super().add_field(node, to_field=to_field)
        self.addChild(node)

    def remove_field(self, node: BaseFieldItem, **kwargs):
        super().remove_field(node, **kwargs)
        self.removeChild(node)

    @property
    def data2(self):
        """Remove field data setting."""
        return None

    @data2.setter
    def data2(self, value):
        pass


class FieldTreeWidget(
        CommonComponent, QTreeWidget, metaclass=BaseTreeWidgetMeta):
    """
    Tree widget for the treeview.

    This manages the widget initialization and the
    fieldui editing (triggered by mouse double click).
    """

    loggername = "qtui.fieldviews.tree.widget"

    def __init__(self,
                 rootfield: RootField,
                 view: RootFieldUI,
                 *args,
                 parent: QWidget = None,
                 **kwargs):

        self.rootfield = rootfield
        self.current_edit = None
        self.current_add = None
        super().__init__(parent=parent)
        self.ctxmenu = TreeItemMenu(self)
        self.ctxmenu.init_ui()
        self.view = view

        # TODO: use settings for shortcuts
        self.shortcuts = [(QShortcut(QKeySequence(Qt.Key_Escape), self),
                           self.esc_reset_selection)]

    def init_ui(self, src_wid: QTreeWidget = None):
        """Init tree and tranfer widget property from source to self."""
        # tree configuration tranfer
        if src_wid is not None:
            tranfer_properties(
                src_wid,
                self,
                exclude=("header", "headerItem", "itemDelegate", "parent",
                         "columnWidth", "expanded", "indexWidget",
                         "itemDelegateForColumn", "itemDelegateForRow",
                         "itemExpanded", "itemWidget", "model", "property",
                         "selectionModel"))

            for i in range(src_wid.headerItem().columnCount()):
                self.headerItem().setText(i, src_wid.headerItem().text(i))

        # signals
        self.itemDoubleClicked.connect(self.on_double_click)
        self.customContextMenuRequested.connect(self.ctxmenu.on_context_menu)

        for shortcut, slot in self.shortcuts:
            shortcut.activated.connect(slot)

        # mainwindow
        mainwindow = get_main_window()
        actions = [
            (mainwindow.action_add, self.open_add_dialog),
            (mainwindow.action_delete, self.canc_remove_field),
        ]

        for action, slot in actions:
            action.triggered.connect(slot)

    def show(self):
        self.setVisible(True)
        super().show()

    def close(self):
        self.deleteLater()

    # overrides
    def remove_field(self, item: BaseFieldItem, **kwargs):
        """A shorthand for self.parent().remove_field."""
        if self.isVisible():
            self.invisibleRootItem().removeChild(item)
            self.view.remove_field(item, **kwargs)

    # slots
    @Slot(QTreeWidgetItem, int)
    def on_double_click(self, item: QTreeWidgetItem, index: int):
        """Create a temp edit for item columns."""
        if self.current_edit is not None and self.current_edit.end:
            self.current_edit = None

        if self.current_edit is None and (
                not isinstance(item, IterableFieldItem) or index == 0):

            if index == 0:
                wid = QLineEdit(parent=self)
                wid.setText(item.field.name)
                field_property = "name"

            elif index == 1:
                wid = field_to_widget(item.field, parent=self)
                field_property = "data"

            wid = GenericInputWrapper.generate_wrapper(
                wid, field=item.field, field_property=field_property)

            self.current_edit = TempEditWrapper(item, index, wid)

    # shortcuts slots
    def open_add_dialog(self):
        """Add an element on canc."""
        # discard slot if not valid, no error dialog will be showed.

        if not self.isVisible():
            pass

        elif self.current_add is not None:
            self.logger.warning("Another add is running.")

        else:
            selected_items = self.selectedItems()
            if selected_items:
                is_tree = False

            elif self.view.tree is None:
                self.logger.warning(
                    "The file is not loaded completely, show a warning message."
                )
                QMessageBox.warning(
                    self,
                    tr(self.objectName(), "File not loaded"),
                    tr(self.objectName(), "Please wait for loading"),
                )
                return

            else:
                selected_items.append(self.view.tree)
                is_tree = True

            if len(selected_items) > 1:
                self.logger.warning(
                    "Too many elements are selected, show a warning message.")
                QMessageBox.warning(
                    self,
                    tr(self.objectName(), "Too many selected items"),
                    tr(self.objectName(), "Please select only one field."),
                )

            # after this, there is only one selected item
            elif not isinstance(selected_items[0], IterableFieldItem):
                self.logger.warning(
                    "The element is not indexable/a container, show a warning message."
                )
                QMessageBox.warning(
                    self,
                    tr(self.objectName(), "Not a container field"),
                    tr(
                        self.objectName(), "Can't add a new field into this\n"
                        "Please select a container field."),
                )

            else:
                selected_item = selected_items[0]
                self.current_add = NewFieldDialog(selected_item, parentwid=self)
                self.current_add.show()
                self.current_add.exec_()
                if is_tree and not self.current_add.rejected:
                    child = selected_item.children[-1]
                    selected_item.removeChild(child)
                    self.addTopLevelItem(child)
                self.current_add = None

    def canc_remove_field(self):
        """Remove element on canc, it will delete the selected item."""
        for item in self.selectedItems():
            if item.parent() is None:
                self.remove_field(item, from_field=True)
            else:
                item.parent().remove_field(item, from_field=True)

    def esc_reset_selection(self):
        """Clear selection on esc."""
        self.clearSelection()
        self.setCurrentItem(None)


class TreeView(RootFieldUI, Ui_TreeView, QFrame, metaclass=BaseFrameMeta):

    loggername = "qtui.fieldviews.tree"

    def __init__(self,
                 rootfield: RootField,
                 *args,
                 parent: QWidget = None,
                 **kwargs):
        super().__init__(parent=parent)
        self.settings = SettingsManager.factory(None)
        self.treewid = FieldTreeWidget(rootfield, self)
        self.editwid = FieldDetailsView(self)

    def _background_loading(self):
        # create generator
        gentree = self.ui_builder(
            self.treewid.rootfield, transformer=_ui_tranformer, lazy=True)
        # self.tree = next(gentree)

        callback = lambda item: item.show()

        load_type = self.settings.qtdebug.get("load type", "default")
        if load_type in ("default", "python"):
            # python threading pool
            with ThreadPool() as pool:
                pool.map(callback, gentree)

        elif load_type == "qt":
            # qt based threading pool
            pool = QThreadPool.globalInstance()
            for item in gentree:
                runnable = RunnableWrapper(callback, item)

                pool.start(runnable)

        else:
            raise NotImplementedError(
                "Load type {} isn't implemented".format(load_type))

        # add root children to treewid
        for child in self.tree.takeChildren():
            # pool.start(RunnableWrapper(self.treewid.addTopLevelItem, child))
            self.treewid.addTopLevelItem(child)

        gc.collect()

    def init_ui(self):

        super().init_ui()

        self.setupUi(self)

        # children init_ui
        self.treewid.init_ui(self.fieldtree)
        self.editwid.init_ui()

        # edit splitter
        self.splitter.replaceWidget(0, self.treewid)
        self.splitter.addWidget(self.editwid)
        self.splitter.setSizes([1, 250])

        # init tree
        Thread(target=self._background_loading, daemon=True).start()

        # cleanup temp frame
        self.fieldtree.deleteLater()
        del self.fieldtree

        # bind signals
        self.treewid.currentItemChanged.connect(self.on_item_selected)

    def show(self):
        """Show self and its children."""
        super().show()

        # show children
        self.treewid.show()
        self.editwid.show()

        # self.editwid.resize(1, 1)

    def close(self):
        self.close_all()
        self.treewid.close()
        self.editwid.close()

    @Slot(QTreeWidgetItem, QTreeWidgetItem)
    def on_item_selected(self, current: BaseFieldItem, _: BaseFieldItem):
        """If an item is selected, change the detalis view."""

        if current is None:
            self.editwid.current_field = None
        else:
            self.editwid.current_field = current.field


_ui_tranformer = OrderedDict([
    (IndexableField, IterableFieldItem),
    # (NameField, NameFieldItem),
    # (BoolField, BoolFieldItem),
    # (IntField, NumericFieldItem),
    # (FloatField, NumericFieldItem),
    # (StringField, StringFieldItem),
    (Field, BaseFieldItem),
])
