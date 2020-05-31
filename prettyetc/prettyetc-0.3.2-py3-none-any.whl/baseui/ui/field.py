#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Field tree and single node UI basic representations.

This module provides a tree-based and extensible UI structure,
by a RootField UI and single Field UIs.

.. versionadded:: 0.3.0
"""

# pylint: disable=W0223

from collections import OrderedDict

from prettyetc.etccore.langlib import Field, IndexableField
from prettyetc.etccore.langlib.root import RootField
from prettyetc.etccore.logger import errhelper

from .common import CommonComponent


class BaseFieldUI(CommonComponent):
    """
    Basic representations of a :class:`~prettyetc.etccore.langlib.Field` UI.

    .. versionadded:: 0.3.0
    """

    def __init__(self, field: Field, *args, **kwargs):
        self.field = field
        super(BaseFieldUI, self).__init__(*args, **kwargs)

    def __repr__(self):
        """Represent field stored."""
        return "<{} field={}>".format(
            type(self).__name__,
            type(self.field).__name__)


class IndexableFieldUI(BaseFieldUI):
    """
    Basic representations of a :class:`~prettyetc.etccore.langlib.IndexableField` UI.

    .. versionadded:: 0.3.0
    """

    def __init__(self, field: IndexableField, *args, children=None, **kwargs):
        super().__init__(field, *args, **kwargs)
        if children is None:
            self.children = []
        else:
            self.children = children

    def __iter__(self):
        """Iterate over children."""
        return self.children.__iter__()

    def __repr__(self):
        """Represent field stored and its children."""
        return "<{} field={} children={}>".format(
            type(self).__name__, self.field, self.children)

    def add_field(self, fieldui: BaseFieldUI):
        """
        Add new field UI to children list.

        .. note::
            This methods doesn't change the
            :class:`~prettyetc.etccore.langlib.Field` object.
        """
        self.children.append(fieldui)


class RootFieldUI(CommonComponent):
    """
    Basic representations of a :class:`~prettyetc.etccore.langlib.RootField` UI.

    It helps the UI to manipulate the field tree and the associated
    :class:`~BaseFieldUI` object tree, by providing a tree builder
    (:meth:`~RootFieldUI.ui_builder`) and a tree extractor
    (:meth:`~RootFieldUI.root_extractor`).

    .. versionadded:: 0.3.0
    """
    loggername = "baseui.ui.field.root"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tree = None

    def ui_builder(self,
                   rootfield: RootField,
                   extra_args: tuple = (),
                   transformer: OrderedDict = None,
                   extra_kwargs: dict = None):
        """
        Build an Ui tree, using :class:`~BaseFieldUI` object, from
        :class:`~prettyetc.etccore.langlib.root.RootField` object,
        using a field transformer if avaiable.

        :param prettyetc.etccore.langlib.root.RootField rootfield:
            The root field to convert to :class:`~BaseFieldUI` object tree.

        :param transformer:
            An object that converts :class:`~prettyetc.etccore.langlib.Field`
            to :class:`~BaseFieldUI` object.

            The transformer can be a callable that must accept a field parameter and
            must return a :class:`~BaseFieldUI` object. Extra arguments can be given
            through extra_args and extra_kwargs parameters.

            The transformer can be also a dict-like object
            where keys are Field or subclasses objects and values are
            associated BaseFieldUI objects.
            Dict items order expects to be from Field most specialized class to
            the Field class itself due to isinstance calls,
            therefore we suggests to use collections.OrderedDict.

        :type transformer: OrderedDict (or dict but discouraged) or callable, optional

        :param tuple extra_args: Extra positional parameters given to transformer.

        :param dict extra_kwargs: Extra positional parameters given to transformer.

        """

        # default transformer
        def _dict_transformer(field, *args, **kwargs) -> BaseFieldUI:
            """Convert given field to a BaseFieldUI object."""

            try:
                # try direct association
                uitype = transform_map[type(field)]

            except KeyError:
                # fallback to a for loop
                for fieldtype, uitype in transform_map.items():
                    if isinstance(field, fieldtype):
                        break
                else:
                    self.logger.warning("No UI type found for %s object.",
                                        type(field).__name__)
            return uitype(field, *args, **kwargs)

        # ui tree builer
        def _recursive_builder(
                indexable_field: IndexableField) -> IndexableFieldUI:
            fieldui = transformer(indexable_field, *extra_args, **extra_kwargs)
            for field in indexable_field:
                if isinstance(field, IndexableField):
                    child_fieldui = _recursive_builder(field)
                else:
                    child_fieldui = transformer(field, *extra_args,
                                                **extra_kwargs)
                fieldui.add_field(child_fieldui)
            return fieldui

        # method body
        if extra_kwargs is None:
            extra_kwargs = {}

        if transformer is None:
            transform_map = OrderedDict([(IndexableField, IndexableFieldUI),
                                         (Field, BaseFieldUI)])
            transformer = _dict_transformer

        elif isinstance(transformer, dict):
            transform_map = transformer
            transformer = _dict_transformer

        elif not callable(transformer):
            self.logger.error(
                "Given transformer is not a callable or a dict-like object (got %s)",
                type(transformer).__name__)

        rootui = _recursive_builder(rootfield)
        self.tree = rootui

    def _call_to_tree(self, methodname: str, exclude_root: bool = False):
        """Call each Field UI items method in the tree by method name."""

        def _recursive_caller(fieldui: IndexableFieldUI):
            getattr(fieldui, methodname)()
            for child in fieldui:
                if isinstance(child, IndexableFieldUI):
                    _recursive_caller(child)
                else:
                    getattr(child, methodname)()

            return fieldui

        if self.tree is None:
            raise errhelper(
                ValueError("Field tree is not initialized."), self.logger)

        if exclude_root:
            for child in self.tree:
                if isinstance(child, IndexableFieldUI):
                    _recursive_caller(child)
                else:
                    getattr(child, methodname)()
        else:
            _recursive_caller(self.tree)

    def init_ui_all(self, exclude_root: bool = False):
        """Init all Field UI items in the tree by calling its init_ui method."""
        self._call_to_tree("init_ui", exclude_root=exclude_root)

    def show_all(self, exclude_root: bool = False):
        """Show all Field UI items in the tree by calling its show method."""
        self._call_to_tree("show", exclude_root=exclude_root)

    def close_all(self, exclude_root: bool = False):
        """Close all Field UI items in the tree by calling its close method."""
        self._call_to_tree("close", exclude_root=exclude_root)
