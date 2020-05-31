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
import pickle

from . import ArrayField, Field, NestedField

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
        This parameter is saved into
        :attr:`~Field.attributes`.

        .. deprecated:: 0.2.0
            Use the langname parameter instead.

    :param str langname:
        Represents the language of the tree.
        This parameter is saved into :attr:`~Field.attributes`.

        .. versionadded:: 0.2.0

    .. versionchanged:: 0.2.0
        Class moved to :mod:`~prettyetc.etccore.langlib.root` module.
        Add pickle support.
    """

    __slots__ = ("typeconf", )

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
                 typeconf="",
                 metadata=None,
                 **kwargs):

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
