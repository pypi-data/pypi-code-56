#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Root fields module.

A root field is a special :class:`.Field`
that represents the root node of the :class:`.Field` tree.
Usually, the root field contains all the parsed fields of a configuration file.

That's a summary of basic root field types.

:class:`~RootField`
-----------------------------------------
This is the simplest and basic root field.
It handles :class:`.Field` objects as a tree.


.. versionadded:: 0.2.0
"""
import os
import pickle
import sys
from functools import partial
from multiprocessing import Manager as ProcessManager
from multiprocessing import cpu_count
from multiprocessing.pool import Pool, ThreadPool

from .field import ArrayField, DictField, Field, IndexableField, NestedField

__all__ = ("RootField", "TableRootField")

if sys.version_info < (3, 5):
    # Python 3.4 raises a pickle error
    Pool = ThreadPool


# RootField.find_by_attr
def _not_check_all(field: Field, force_string: bool, **attributes) -> bool:
    for key, val in attributes.items():
        attrval = getattr(field, key, None)
        if hasattr(field, key) and (str(attrval)
                                    if force_string else attrval) == val:
            return True
    return False


def _check_all(field: Field, force_string: bool, **attributes) -> bool:
    for key, val in attributes.items():
        attrval = getattr(field, key, None)
        if not (hasattr(field, key) and (str(attrval)
                                         if force_string else attrval) == val):
            return False
    return True


class RootField(NestedField):
    """
    Represents the root of the field tree.
    Depending on the parsed language,
    root elements can be contained into a :class:`list` or a :class:`dict`.

    This class should be used (and in some cases, reimplemented)
    for other types of RootField.

    :param dict metadata: An alias for the attributes parameter.

        .. deprecated:: 0.2.0
            Use the attributes parameter instead.

    :param str typeconf: An alias for the langname parameter.
        This parameter is saved into :attr:`.Field.attributes`.

        .. deprecated:: 0.2.0
            Use the langname parameter instead.

    :param str langname:
        Represents the language of the tree.
        This parameter is saved into :attr:`.Field.attributes`.

        .. versionadded:: 0.2.0

    :param str source: The parsed string that is represented in the tree

    .. versionchanged:: 0.2.0

        Class moved to :mod:`prettyetc.etccore.langlib.root` module.

        Add pickle support.
    """

    __slots__ = ("typeconf", "_source")

    @classmethod
    def from_pickle(cls, pkin) -> Field:
        """
        Load field tree from given stream.

        .. versionadded:: 0.2.0
        """
        try:
            return pickle.load(pkin)
        except pickle.UnpicklingError:
            return None

    def to_pickle(self, out) -> bool:
        """
        Dump field tree to given stream.

        .. versionadded:: 0.2.0
        """
        pickle.dump(self, out, protocol=pickle.HIGHEST_PROTOCOL)

    def __init__(self,
                 *args,
                 langname: str = "",
                 source: str = None,
                 typeconf="",
                 metadata=None,
                 **kwargs):

        self._source = source
        # 0.1.x compatibility
        if kwargs.get("attributes") is None and metadata is not None:
            kwargs["attributes"] = metadata

        super().__init__(*args, **kwargs)

        # 0.1.x compatibility
        new_attrs = self.attributes.copy()
        new_attrs["langname"] = langname if langname else typeconf
        self.attributes = new_attrs
        self.typeconf = self.attributes["langname"]

    # IndexableField reimplementation
    def add(self, other: Field):
        if isinstance(self.data, list):
            return ArrayField.add(self, other)

        if isinstance(self.data, Field):
            return self.data.add(self, other)

        return super().add(other)

    def remove(self, other: Field):
        if isinstance(self.data, list):
            return ArrayField.remove(self, other)

        if isinstance(self.data, Field):
            return self.data.remove(self, other)

        return super().remove(other)

    def iteritems(self) -> iter:
        if isinstance(self.data, dict):
            return DictField.iteritems(self)
        return super().iteritems()

    @property
    def source(self) -> str:
        """
        Get the source of configuration file.

        If available, the source file is the setted source.
        If name is the file path, the file content is read and saved into source.

        If none of these are available, a ValueError is raised.

        :raises ValueError: If source is not available
        """
        if getattr(self, "_source", None) is not None:
            return self._source

        if self.name is not None and os.path.isfile(self.name):
            with open(self.name) as stream:
                self.source = stream.read()

            return self._source

        raise ValueError("Source is not available")

    @source.setter
    def source(self, value: str):
        """The source property setter."""
        self._source = value

    @source.deleter
    def source(self):
        """The source property deleter."""
        del self._source

    metadata = NestedField.attributes
    """
    An alias for :obj:`.Field.attributes`.

    .. deprecated:: 0.3.0
        Use :obj:`.Field.attributes` instead.
    """

    # util methods
    def find_by_attr(self,
                     multiple_fields: bool = False,
                     force_string: bool = False,
                     check_all: bool = True,
                     parallel: bool = False,
                     **attributes):
        """
        Find :class:`~prettyetc.etccore.langlib.field.Field` objects by given attributes.

        It finds the given attributes
        in each :class:`~prettyetc.etccore.langlib.field.Field` objects in the tree,
        iterating recursively each
        :class:`~prettyetc.etccore.langlib.field.IndexableField` objects.

        If one of attribute was not found, the whole field is not equals.
        If attributes attribute is given, this method will check
        if given attributes dict items are in field attributes dict.

        By default, this return the first occurrence of field unless you set
        the multiple_fields parameter to True.

        :param bool multiple_fields: Return each occurrence of field with given attributes.

        :param bool force_string: Force all attributes checks to be strings
                                  (given attributes values should be strings).

        :param bool check_all: If True, all the attributes are checked, false otherwise.

        :param bool parallel:
            If True, processes (or threads if :obj:`~.Field.data` is small)
            are used to speed up the operation.

            .. versionadded:: 0.4.0

        .. versionadded:: 0.3.0
        """

        if check_all:
            # check all attributes
            predicate = _check_all
        else:
            # check only one attribute
            predicate = _not_check_all

        iterable = self._data
        if isinstance(self._data, dict):
            iterable = self._data.values()

        if parallel:
            if len(self.data) < cpu_count():
                retfield = []
                if not multiple_fields:
                    retfield.append(None)
                with ThreadPool() as pool:
                    pool.map(
                        partial(RootField._recursive_finder, force_string,
                                predicate, retfield, **attributes),
                        iterable,
                    )
            else:
                with ProcessManager() as manager:
                    retfield = manager.list()
                    if not multiple_fields:
                        retfield.append(None)
                    with Pool() as pool:
                        pool.map(
                            partial(RootField._recursive_finder, force_string,
                                    predicate, retfield, **attributes),
                            iterable)
                    retfield = list(retfield)

        else:
            retfield = []
            if not multiple_fields:
                retfield.append(None)
            for fld in iterable:
                RootField._recursive_finder(force_string, predicate, retfield,
                                            fld, **attributes)

        if multiple_fields:
            return retfield

        return retfield[0]

    @staticmethod
    def _recursive_finder(force_string: str, predicate: callable,
                          retfield: list, field: Field, **attributes):
        if predicate(field, force_string, **attributes):
            if retfield and retfield[0] is None:
                retfield[0] = field
                return True
            retfield.append(field)

        if isinstance(field, IndexableField):
            for fld in field:
                ret = RootField._recursive_finder(force_string, predicate,
                                                  retfield, fld, **attributes)
                if ret is True:
                    return True
        return None


class TableRootField(RootField):
    """
    Representing the field view as a column labelled table.

    This class is useful for configuration languages that doesn't
    represent data as a tree, but as a table, such as CSV.

    Internal data structure is a dict,
    for each label is associated an :class:`~prettyetc.etccore.langlib.field.ArrayField`.
    To manipulate data use the sequence protocol and the :meth:`~TableRootField.add_col` method.
    Direct access to data is still supported to maintain the field philosophy.

    :param data:
        This parameter is overridden to an empty dict.
        Set data using properly methods.

    .. versionadded:: 0.2.0
    """

    def __init__(self, *args, **kwargs):
        kwargs["data"] = {}
        super().__init__(*args, **kwargs)

    def add_col(self,
                name,
                *items: Field,
                description: str = "",
                attributes: dict = None,
                readonly: bool = False) -> ArrayField:
        """
        Add a column to the table.

        If a column with given name already exists,
        the old column will be silently replaced with a new one.

        :return: The :class:`.ArrayField`
                 object associated to the column.
        """
        data = ArrayField(
            name,
            data=list(items),
            description=description,
            attributes=attributes,
            readonly=readonly)
        self[name] = data
        return data

    def del_col(self, name):
        """
        Remove a column in the table.

        :raises KeyError: If column with given name doesn't exists.
        """
        del self[name]
