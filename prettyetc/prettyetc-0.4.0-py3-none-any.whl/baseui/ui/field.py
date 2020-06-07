#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Field tree and single node UI basic representations.

This module provides a tree-based and extensible UI structure for a
RootField UI and Field UI.

.. versionadded:: 0.3.0
"""

# pylint: disable=W0223
from collections import OrderedDict
from multiprocessing.pool import ThreadPool as Pool

from prettyetc.etccore.langlib import Field, IndexableField
from prettyetc.etccore.langlib.root import RootField
from prettyetc.etccore.logger import errhelper

from .common import CommonComponent


class BaseFieldUI(CommonComponent):
    """
    Basic UI representation of a :class:`.Field` object.
    As for fields, the objects of this class should be represented in a tree.

    .. note::
        Some times we call a :class:`.BaseFieldUI` object "fieldui".

    :param Field field: the field to be wrapped.

    .. versionadded:: 0.3.0
    """

    def __init__(self, field: Field, *args, **kwargs):
        self.field = field
        """Represented :class:`.Field` object."""

        super(BaseFieldUI, self).__init__(*args, **kwargs)

    def __repr__(self):
        """Represent field stored."""
        return "<{} field={}>".format(
            type(self).__name__,
            type(self.field).__name__,
        )

    def save(self):
        """
        Save fields attributes into field.

        This method should be overridden when field attribute
        are not automatically saved into field.

        By default, it does nothing.

        .. versionadded:: 0.4.0
        """


class IndexableFieldUI(BaseFieldUI):
    """
    Basic UI representation of an :class:`.IndexableField` object.

    :param list children: A list of :class:`BaseFieldUI` objects.

    .. versionadded:: 0.3.0
    """

    @classmethod
    def create_child(cls,
                     field: Field,
                     transformer: OrderedDict = None,
                     extra_args: tuple = (),
                     extra_kwargs: dict = None):
        """
        Create a new fieldui from given field.

        :param collections.OrderedDict transformer:
            An object that converts :class:`.Field`
            to a :class:`~BaseFieldUI` object.

            The transformer can be a callable that must accept a field parameter and
            must return a :class:`~BaseFieldUI` object. Extra arguments can be given
            through extra_args and extra_kwargs parameters.

            The transformer can also be a dict-like object
            where keys are :class:`~prettyetc.etccore.langlib.field.Field` or
            subclasses objects and values are associated :class:`~BaseFieldUI` objects.
            Dict items should be sorted from the most specialized Field (subclass) to
            the less specialized Field (subclass) due to :func:`isinstance` calls,
            therefore we suggests to use collections.OrderedDict.

        :param tuple extra_args: Extra positional parameters given to transformer.

        :param dict extra_kwargs: Extra positional parameters given to transformer.

        .. versionadded:: 0.4.0
        """

        # method body
        if extra_kwargs is None:
            extra_kwargs = {}

        if transformer is None:
            transformer = OrderedDict([
                (IndexableField, IndexableFieldUI),
                (Field, BaseFieldUI),
            ])

        if isinstance(transformer, dict):
            transform_map = transformer
            return IndexableFieldUI._dict_transformer(
                field, transform_map, *extra_args, **extra_kwargs)

        return transformer(field, *extra_args, **extra_kwargs)

    @staticmethod
    def _dict_transformer(field, transform_map: dict, *extra_args,
                          **extra_kwargs) -> BaseFieldUI:
        """Convert given field to a BaseFieldUI object."""
        try:
            # try direct association
            uitype = transform_map[type(field)]

        except KeyError:
            # fallback to for loop
            for fieldtype, uitype in transform_map.items():
                if isinstance(field, fieldtype):
                    break
            else:

                return None

        return uitype(field, *extra_args, **extra_kwargs)

    def __init__(self,
                 field: IndexableField,
                 *args,
                 children: list = None,
                 **kwargs):
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
            type(self).__name__,
            self.field,
            self.children,
        )

    def add_field(self, fieldui: BaseFieldUI, to_field: bool = False):
        """
        Add given field UI to children list.

        :param BaseFieldUI fieldui: the child fieldui to be added to self.

        :param bool to_field:
            If True, add given fieldui's field also from :attr:`BaseFieldUI.field`.

            .. versionadded:: 0.4.0

        .. note::
            This method doesn't change :attr:`BaseFieldUI.field`.
        """
        self.children.append(fieldui)
        if to_field:
            self.field.add(fieldui.field)

    def remove_field(self, fieldui: BaseFieldUI, from_field: bool = False):
        """
        Remove given field UI from children list.

        :param BaseFieldUI fieldui: the child fieldui to be removed from self.

        :param bool from_field:
            If True, remove given field UI's field also from :attr:`BaseFieldUI.field`.

        .. versionadded:: 0.4.0
        """
        self.children.remove(fieldui)
        if from_field:
            self.field.remove(fieldui.field)


class RootFieldUI(CommonComponent):
    """
    Basic representations of a :class:`~prettyetc.etccore.langlib.RootField` object,
    using a :class:`~BaseFieldUI` object tree.

    When instanced, the object is useless; you must create a :class:`~BaseFieldUI`
    tree using :meth:`~RootFieldUI.ui_builder`.
    You can get the tree through the :attr:`~RootFieldUI.tree` attribute.

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
                   extra_kwargs: dict = None,
                   lazy: bool = False):
        """
        Build an UI tree, using :class:`~BaseFieldUI` object, from an :class:`.RootField` object,
        using a field transformer (see the tranformer parameter below).
        The built tree will be stored into the :attr:`~RootFieldUI.tree` attribute.

        :param RootField rootfield:
            The root field to be converted to a :class:`~BaseFieldUI` object tree.

        :param transformer:
            An object that converts :class:`.Field`
            to a :class:`~BaseFieldUI` object.

            The transformer can be a callable that must accept a field parameter and
            must return a :class:`~BaseFieldUI` object. Extra arguments can be given
            through extra_args and extra_kwargs parameters.

            The transformer can also be a dict-like object
            where keys are :class:`~prettyetc.etccore.langlib.field.Field` or
            subclasses objects and values are associated :class:`~BaseFieldUI` objects.
            Dict items should be sorted from the most specialized Field (subclass) to
            the less specialized Field (subclass) due to isinstance calls,
            therefore we suggests to use collections.OrderedDict.

        :type transformer: OrderedDict (or dict but discouraged) or callable.

        :param tuple extra_args: Extra positional parameters given to transformer.

        :param dict extra_kwargs: Extra positional parameters given to transformer.

        :param bool lazy: If True, this method return a generator that iterates
                          :class:`~BaseFieldUI` objects of the tree,
                          creates in the iteration step.
        """

        def _gen_wrapper(generator):
            self.tree = yield from generator
            return self.tree

        # ui tree builder
        def _recursive_builder(
                indexable_field: IndexableField) -> IndexableFieldUI:

            # create fieldui container (IndexableFieldUI)
            fieldui = IndexableFieldUI.create_child(
                indexable_field,
                transformer,
                extra_args,
                extra_kwargs,
            )

            if fieldui is None:
                self.logger.warning("No UI type found for %s object.",
                                    type(indexable_field).__name__)
            else:
                # iterate for each field children
                for field in indexable_field:

                    if isinstance(field, IndexableField):
                        builder_iterable = _recursive_builder(field)

                        # child_fieldui = next(builder_iterable)
                        # yield child_fieldui
                        child_fieldui = yield from builder_iterable
                        fieldui.add_field(child_fieldui)

                    else:
                        # create a simple fieldui for non indexable fields
                        child_fieldui = IndexableFieldUI.create_child(
                            field,
                            transformer,
                            extra_args,
                            extra_kwargs,
                        )

                        if child_fieldui is None:
                            self.logger.warning(
                                "No UI type found for %s object.",
                                type(field).__name__)
                        else:
                            # add child to fieldui children
                            fieldui.add_field(child_fieldui)
                            yield child_fieldui

            yield fieldui
            return fieldui

        # set default values for dict-like parameters
        if extra_kwargs is None:
            extra_kwargs = {}

        if transformer is None:
            transformer = OrderedDict([
                (IndexableField, IndexableFieldUI),
                (Field, BaseFieldUI),
            ])

        elif not (callable(transformer) or isinstance(transformer, dict)):
            self.logger.error(
                "Given transformer is not a callable or a dict-like object (got %s)",
                type(transformer).__name__)
            return None

        # create the generator
        ui_generator = _gen_wrapper(_recursive_builder(rootfield))

        if lazy:
            return _gen_wrapper(ui_generator)

        # no lazy
        for _ in _gen_wrapper(ui_generator):
            pass

        return self.tree

    def _call_to_tree(self,
                      methodname: str,
                      exclude_root: bool = False,
                      parallel: bool = False):
        """For each Field UI element in the tree call the method by its name."""

        def _recursive_caller(fieldui: IndexableFieldUI):

            def _step(child):
                if isinstance(child, IndexableFieldUI):
                    _recursive_caller(child)
                else:
                    getattr(child, methodname)()

            getattr(fieldui, methodname)()
            for _ in _map(_step, iter(fieldui)):
                pass
            return fieldui

        if self.tree is None:
            raise errhelper(
                ValueError("Field tree is not initialized."),
                self.logger,
            )

        if parallel:
            pool = Pool()
            _map = pool.map
        else:
            pool = None
            _map = map

        if exclude_root:
            for child in self.tree:
                if isinstance(child, IndexableFieldUI):
                    _recursive_caller(child)
                else:
                    getattr(child, methodname)()
        else:
            _recursive_caller(self.tree)

        if parallel:
            pool.close()

    def init_ui_all(self, exclude_root: bool = False, parallel: bool = False):
        """Init all Field UI items in the tree by calling its init_ui method."""
        self._call_to_tree(
            "init_ui", exclude_root=exclude_root, parallel=parallel)

    def show_all(self, exclude_root: bool = False, parallel: bool = False):
        """Show all Field UI items in the tree by calling its show method."""
        self._call_to_tree("show", exclude_root=exclude_root, parallel=parallel)

    def close_all(self, exclude_root: bool = False, parallel: bool = False):
        """Close all Field UI items in the tree by calling its close method."""
        self._call_to_tree(
            "close", exclude_root=exclude_root, parallel=parallel)

    def add_field(self, fieldui: BaseFieldUI):
        """
        Add new field UI to children list.

        .. note::
            This method doesn't change :attr:`RootFieldUI.tree`.

        .. versionadded:: 0.4.0
        """
        self.tree.add_field(fieldui)

    def remove_field(self, fieldui: BaseFieldUI, from_field: bool = False):
        """
        Remove field UI from children list.

        :param bool from_field:
            If True, remove given field UI field also from :attr:`RootFieldUI.tree`.

        .. versionadded:: 0.4.0
        """
        self.tree.remove_field(fieldui, from_field=from_field)
