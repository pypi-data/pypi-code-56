#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Root fields module.

A root field is a special :class:`~prettyetc.etccore.langlib.Field`
that represent the main container.
A root fields usually represents a configuration file.

That's a summary of basic root field types.

:class:`~RootField`
-----------------------------------------
This is the simplest and basic root field.
It handle fields as a tree.


.. versionadded:: 0.2.0

.. note::
    All fields in this module are avaiable in :mod:`~prettyetc.etccore.langlib`
    for backward compatibility.

"""
import os
import pickle

from .field import ArrayField, Field, IndexableField, NestedField

__all__ = ("RootField", "TableRootField")


class RootField(NestedField):
    """
    Represents the root of the field tree.
    Depending of the language,
    root elements can be represent in a list or in a dict.

    This class should be used (and in some cases, reimplemented)
    for other types of RootField.


    :param dict metadata: An alias for the attributes parameter.

        .. deprecated:: 0.2.0
            Use the attributes parameter instead.

    :param str typeconf: An alias for the langname parameter.
        This parameter is saved into :attr:`~Field.attributes`.

        .. deprecated:: 0.2.0
            Use the langname parameter instead.

    :param str langname:
        Represents the language of the tree.
        This parameter is saved into :attr:`~Field.attributes`.

        .. versionadded:: 0.2.0

    :param str source: The parsed string that is represented in the tree

    .. versionchanged:: 0.2.0
        Class moved to :mod:`~prettyetc.etccore.langlib.root` module.
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
        self._attributes["langname"] = typeconf if langname else langname
        self.typeconf = self._attributes["langname"]

    def to_pickle(self, out) -> bool:
        """
        Dump field tree to given stream.

        .. versionadded:: 0.2.0
        """
        pickle.dump(self, out, protocol=pickle.HIGHEST_PROTOCOL)

    @property
    def source(self) -> str:
        """
        Get the source of configuration file.

        If avaiable, the source file is the setted source.
        If name is the file path, the file content is read and saved into source.

        If none of these are avaiable, a ValueError is raised.

        :raises ValueError: if source is not avaiable
        """
        if self._source is not None:
            return self._source

        if os.path.isfile(self.name):
            with open(self.name) as stream:
                self.source = stream.read()

            return self._source

        raise ValueError("Source is not avaiable")

    @source.setter
    def source(self, value: str):
        """The source property setter."""
        self._source = value

    @source.deleter
    def source(self):
        """The source property deleter."""
        del self._source

    """
    .. deprecated:: 0.3.0
        Use attributes attribute
    """
    metadata = NestedField.attributes

    # util methods
    def find_by_attr(self,
                     multiple_fields: bool = False,
                     force_string: bool = False,
                     check_all: bool = True,
                     **attributes):
        """
        Find :class:`~prettyetc.etccore.langlib.field.Field` by given attributes.

        It finds the given attributes
        in every :class:`~prettyetc.etccore.langlib.field.Field` in tree,
        iterating recursively
        :class:`~prettyetc.etccore.langlib.field.IndexableField` when appears.

        If one of attribute was not found, the whole field is not equals.
        If attributes attribute is given, this method will check
        if given attributes dict items are in field attributes dict.

        By default this return the first occurence of field unless you set
        the multiple_fields parameter to True.

        :param bool multiple_fields: Return each occurence of field with given attributes.
        :param bool force_string: Force all attributes checks to be strings
                                  (given attributes values should be strings).
        :param bool check_all: If True, all the attributes are checked, false otherwise

        .. versionadded:: 0.3.0
        """

        def _not_check_all(field: Field) -> bool:
            for key, val in attributes.items():
                attrval = getattr(field, key, None)
                if hasattr(field, key) and (str(attrval) if force_string else
                                            attrval) == val:
                    return True
            return False

        def _check_all(field: Field) -> bool:
            for key, val in attributes.items():
                attrval = getattr(field, key, None)
                if not (hasattr(field, key) and
                        (str(attrval) if force_string else attrval) == val):
                    return False
            return True

        def _recursive_finder(field: Field):
            if predicate(field):
                if retfield.val is None:
                    retfield.val = field
                    return True
                if isinstance(retfield.val, list):
                    retfield.val.append(field)

            if isinstance(field, IndexableField):
                for fld in field:
                    ret = _recursive_finder(fld)
                    if ret is True:
                        return True
            return None

        if multiple_fields:
            retfield = type("", (), {"val": []})()
        else:
            retfield = type("", (), {"val": None})()

        if check_all:
            # check all attributes
            predicate = _check_all
        else:
            # check only one attribute
            predicate = _not_check_all

        if isinstance(self._data, dict):
            for fld in self._data.values():
                _recursive_finder(fld)
        else:
            for fld in self._data:
                _recursive_finder(fld)

        return retfield.val


class TableRootField(RootField):
    """
    Representing the field view as a column-labeled table.

    This class is useful for configuration languages that doesn't
    represents data as a tree, but as a table, such as csv.

    Internal data structure is a dict,
    for each labels is associated an
    :class:`~prettyetc.etccore.langlib.ArrayField`.
    To manipulate data use the sequence protocol and the,
    :meth:`~TableRootField.add_col` method.
    Direct access and manipulating data is still supported to preserve the
    field philosophy.

    :param data:
        This parameter is overriden to an empty dict.
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

        :return ArrayField: The :class:`~prettyetc.etccore.langlib.ArrayField`
                            associated to the column.
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

        :raises KeyError: if column with given name doesn't exists.
        """
        del self[name]
