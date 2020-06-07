#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=====
Field
=====


This module contains all builtins field types.
All of these fields can be extended or joint together.
However, user-defined fields must inherit at least
:class:`~Field` for basic types, or :class:`~IndexableField` for collections.

That's a summary of basic field types available.

:class:`~Field`
-----------------------------------------
This is the base class for all fields in this module
This class is considered the smallest element of a configuration file.


:class:`~TypedField`
----------------------------------------------
This makes type controls in given data,
raising an error if the given data has a wrong type.


:class:`~IndexableField`
--------------------------------------------------
This allows a field to have children of fields
The data of an :class:`~IndexableField` can be a list, a dict, or something else.

:class:`~NameField`
---------------------------------------------
This field has no data.
"""

__all__ = ("Field", "SeparatedField", "NameField", "DataField",
           "IndexableField", "NestedField", "TypedField", "StringField",
           "IntField", "FloatField", "BoolField", "ArrayField", "DictField",
           "StringSeparatedField", "ReadonlyException")
import copy
import operator
import os
from collections import OrderedDict

NoneType = type(None)


class ReadonlyException(Exception):
    """Raised when field is readonly."""


def data_decorator(cls: type):
    """Create data property from methods."""
    cls.data = property(
        fget=cls.getData, fset=cls.setData, fdel=cls.delData, doc="Field data.")
    return cls


def _binaryop_decorator(method_name: str,
                        return_self: bool = True,
                        **extra_params):
    """Create an operator by giving operator name"""

    def wrapper(self, other):
        if extra_params.get("operator") is not None:
            oper = extra_params["operator"]
        elif hasattr(self.data, method_name):
            oper = extra_params["operator"] = getattr(self.data, method_name)
        elif hasattr(operator, method_name):
            oper = extra_params["operator"] = getattr(operator, method_name)
        else:
            raise TypeError("Unsupported method {}.".format(method_name))

        if isinstance(other, Field):
            res = oper(other.data)
        else:
            res = oper(other)

        if return_self:
            newfield = copy.copy(self)
            newfield.attrs = self.attrs.copy()
            newfield.data = res
            return newfield

        if res is not None:
            self.data = res
        return None

    extra_params.setdefault("method_name", method_name)
    extra_params.setdefault("modifier", " ")
    extra_params.setdefault("optype", "operator")
    extra_params.setdefault("exctype", "TypeError")
    wrapper.__doc__ = """
    Do{modifier}{opname} (the '{operator}' {optype}) to the data
    field using a field or any object.

    :raises {exctype}: If {opname} is not possible.

    .. seealso:: :meth:`object.{method_name}`

    .. versionadded:: 0.4.0
    """.format(**extra_params)
    extra_params.clear()
    return wrapper


# simple fields
@data_decorator
class Field(object):
    """
    Basic representation of a generic field.

    All the field's attributes are managed here.

    In addition, the :class:`.Field` class provides a simple event manager,
    based on change of any field attribute;

    Setting a new listener is simple, you just assign the function to
    listener variable.

    .. code::

        def foo(value, valuetype):
            # whatever you want
        field.listener = foo
        print(field.listener)  # [<function foo at 0xnnnnnnnnnnnn>]

    However, you can manipulate directly the listener value,
    but is unsafe because the listener property setter
    make validations in the given callable.

    .. seealso::
        :ref:`API glossary` for a detailed description about what is a
        field and a detailed description of its attributes.

    .. seealso::
        The :meth:`Field.dispatch` method for more information about the event system.

    .. versionchanged:: 0.2.0
        Add field attribute :obj:`~Field.attributes`.

        Add data converters and comparison operators.

    .. versionchanged:: 0.4.0
        Add arithmetic and bitwise operators.
    """

    __slots__ = ("_name", "_description", "_data", "_attributes", "readonly",
                 "_listeners")
    data = None

    _default_datatypes = OrderedDict()

    @classmethod
    def from_primitive(cls,
                       obj,
                       name,
                       fieldtypes: dict = None,
                       description: str = "",
                       readonly: bool = False,
                       **attributes):
        """
        Create an :class:`~Field` instance from a Python primitive.

        .. warning::
            This function can accept iterable data without throwing any error,
            but returns a wrong field.
            So, we suggest to check if the object is iterable before using this method,
            or wrap it in a :class:`list` and pass it to :meth:`.IndexableField.from_primitives`.

        .. versionadded:: 0.4.0
        """

        def _type_checker(fieldkey, fieldval):
            """Check field type and encapsulate key and val into specific field instance."""
            try:
                # try direct association
                final_fieldtype = fieldtypes[type(fieldval)]

            except KeyError:
                # fallback to for loop
                for datatype, fieldtype in fieldtypes.items():
                    if isinstance(fieldval, datatype):
                        final_fieldtype = fieldtype
                        break
                else:
                    raise NotImplementedError(
                        "Unimplemented data type {} of {}".format(
                            type(fieldval), fieldval))
                fieldinst = final_fieldtype(
                    name=fieldkey,
                    data=fieldval,
                    description=description,
                    readonly=readonly,
                    **attributes)
            return fieldinst

        if fieldtypes is None:
            fieldtypes = cls._default_datatypes

        retfield = _type_checker(name, obj)
        return retfield

    def __init__(self,
                 name,
                 data=None,
                 description: str = "",
                 attributes: dict = None,
                 readonly: bool = False):
        super().__init__()
        self._listeners = []

        self._name = name
        self._description = description
        self._data = data

        if not isinstance(attributes, (dict, NoneType)):
            raise TypeError(
                "Field attributes must be a dict or a subclass of it.")
        self.attributes = attributes

        self.readonly = readonly
        """Field readonly flag."""

    def __repr__(self):
        """Generate object representation."""
        template = "<{} {}={}{}>"
        extras = " "

        if self.description:
            extras += "{} ".format(self.description)

        if self.attributes:
            extras += "{} ".format(self.attributes)

        if self.readonly:
            extras += "{} ".format(self.readonly)

        extras = extras.rstrip()
        return template.format(
            type(self).__name__, self.name, self._data, extras)

    # data converts
    def __str__(self) -> str:
        """
        Get data as :class:`str`.

        :raises ValueError: If :obj:`~Field.data` is not convertible to str.

        .. seealso:: :meth:`object.__str__`

        .. versionadded:: 0.2.0
        """
        return str(self._data)

    def __bool__(self) -> bool:
        """
        Get data as :class:`bool`.

        :raises ValueError: If :obj:`~Field.data` is not convertible to bool.

        .. seealso:: :meth:`object.__bool__`

        .. versionadded:: 0.2.0
        """
        return bool(self._data)

    def __int__(self) -> int:
        """
        Get data as :class:`int`.

        :raises ValueError: If :obj:`~Field.data` is not convertible to int.

        .. seealso:: :meth:`object.__int__`

        .. versionadded:: 0.2.0
        """
        return int(self._data)

    def __float__(self) -> float:
        """
        Get data as :class:`float`.

        :raises ValueError: If :obj:`~Field.data` is not convertible to float.

        .. seealso:: :meth:`object.__float__`

        .. versionadded:: 0.2.0
        """
        return float(self._data)

    def __hash__(self) -> int:
        """
        Get data hash.

        :raises TypeError: If :obj:`~Field.data` is unhashable.

        .. seealso:: :meth:`object.__hash__`

        .. versionadded:: 0.2.0
        """
        return hash(self._data)

    # comparison operators
    def __eq__(self, other) -> bool:
        """
        Check field (name and data) equality.

        :raises TypeError: If :obj:`~Field.data` is not comparable.

        .. seealso:: :meth:`object.__eq__`

        .. versionadded:: 0.2.0
        """
        if isinstance(other, Field):
            if self._name == other.name and \
               self._data == other.data:
                # also description can be compared
                # self.description == other.description and \
                return True
        return False

    def __lt__(self, other) -> bool:
        """
        Check if data field is smaller (the '<' operator)
        than the given field data.

        :raises TypeError: If :obj:`~Field.data` is not comparable.

        .. seealso:: :meth:`object.__lt__`

        .. versionadded:: 0.2.0
        """
        if isinstance(other, Field):
            return self._data < other.data
        raise TypeError(
            "'<' not supported between instances of '{}' and '{}'".format(
                type(self).__name__,
                type(other).__name__))

    def __le__(self, other) -> bool:
        """
        Check if data field is smaller or equals (the '<=' operator)
        than the given field data.

        :raises TypeError: If :obj:`~Field.data` is not comparable.

        .. seealso:: :meth:`object.__le__`

        .. versionadded:: 0.2.0
        """
        if isinstance(other, Field):
            return self._data < other.data and self == other
        raise TypeError(
            "'<=' not supported between instances of '{}' and '{}'".format(
                type(self).__name__,
                type(other).__name__))

    def __gt__(self, other) -> bool:
        """
        Check if data field is bigger (the '>' operator)
        than the given field data.

        :raises TypeError: If :obj:`~Field.data` is not comparable.

        .. seealso:: :meth:`object.__gt__`

        .. versionadded:: 0.2.0
        """
        if isinstance(other, Field):
            return self._data < other.data
        raise TypeError(
            "'>' not supported between instances of '{}' and '{}'".format(
                type(self).__name__,
                type(other).__name__))

    def __ge__(self, other) -> bool:
        """
        Check if data field is bigger or equals (the '>=' operator)
        than the given field data.

        :raises TypeError: If :obj:`~Field.data` is not comparable.

        .. seealso:: :meth:`object.__ge__`

        .. versionadded:: 0.2.0
        """
        if isinstance(other, Field):
            return self._data < other.data and self == other
        raise TypeError(
            "'>=' not supported between instances of '{}' and '{}'".format(
                type(self).__name__,
                type(other).__name__))

    # arithmetic operator
    # to do
    __add__ = _binaryop_decorator("__add__", opname="addition", operator="+")
    __radd__ = _binaryop_decorator(
        "__radd__", opname="addition", operator="+", modifier=" (reversed) ")
    __iadd__ = _binaryop_decorator(
        "__iadd__", opname="addition", operator="+", modifier=" in-place ")

    __sub__ = _binaryop_decorator("__sub__", opname="subtraction", operator="-")
    __rsub__ = _binaryop_decorator(
        "__rsub__", opname="subtraction", operator="-", modifier=" (reversed) ")
    __isub__ = _binaryop_decorator(
        "__isub__", opname="subtraction", operator="-", modifier=" in-place ")

    __mul__ = _binaryop_decorator(
        "__mul__", opname="multiplication", operator="*")
    __rmul__ = _binaryop_decorator(
        "__rmul__",
        opname="multiplication",
        operator="*",
        modifier=" (reversed) ")
    __imul__ = _binaryop_decorator(
        "__imul__",
        opname="multiplication",
        operator="*",
        modifier=" in-place ")

    __matmul__ = _binaryop_decorator(
        "__matmul__", opname="matrix multiplication", operator="@")
    __rmatmul__ = _binaryop_decorator(
        "__rmatmul__",
        opname="matrix multiplication",
        operator="@",
        modifier=" (reversed) ")
    __imatmul__ = _binaryop_decorator(
        "__imatmul__",
        opname="matrix multiplication",
        operator="@",
        modifier=" in-place ")

    __truediv__ = _binaryop_decorator(
        "__truediv__", opname="division", operator="/")
    __rtruediv__ = _binaryop_decorator(
        "__rtruediv__",
        opname="division",
        operator="/",
        modifier=" (reversed) ")
    __itruediv__ = _binaryop_decorator(
        "__itruediv__", opname="division", operator="/", modifier=" in-place ")

    __truediv__ = _binaryop_decorator(
        "__truediv__", opname="floor division", operator="//")
    __rtruediv__ = _binaryop_decorator(
        "__rtruediv__",
        opname="floor division",
        operator="//",
        modifier=" (reversed) ")
    __itruediv__ = _binaryop_decorator(
        "__itruediv__",
        opname="floor division",
        operator="//",
        modifier=" in-place ")

    __mod__ = _binaryop_decorator("__mod__", opname="modulo", operator="%")
    __rmod__ = _binaryop_decorator(
        "__rmod__", opname="modulo", operator="%", modifier=" (reversed) ")
    __imod__ = _binaryop_decorator(
        "__imod__", opname="modulo", operator="%", modifier=" in-place ")

    __divmod__ = _binaryop_decorator(
        "__divmod__",
        opname="dimod",
        operator=":func:`divmod`",
        optype="function")
    __rdivmod__ = _binaryop_decorator(
        "__rdivmod__",
        opname="dimod",
        operator=":func:`divmod`",
        optype="function",
        modifier=" (reversed) ")
    __idivmod__ = _binaryop_decorator(
        "__idivmod__",
        opname="dimod",
        operator=":func:`divmod`",
        optype="function",
        modifier=" in-place ")

    __lshift__ = _binaryop_decorator(
        "__lshift__", opname="left shift", operator=">>")
    __rlshift__ = _binaryop_decorator(
        "__rlshift__",
        opname="left shift",
        operator=">>",
        modifier=" (reversed) ")
    __ilshift__ = _binaryop_decorator(
        "__ilshift__",
        opname="left shift",
        operator=">>",
        modifier=" in-place ")

    __rshift__ = _binaryop_decorator(
        "__rshift__", opname="right shift", operator=">>")
    __rrshift__ = _binaryop_decorator(
        "__rrshift__",
        opname="right shift",
        operator=">>",
        modifier=" (reversed) ")
    __irshift__ = _binaryop_decorator(
        "__irshift__",
        opname="right shift",
        operator=">>",
        modifier=" in-place ")

    __and__ = _binaryop_decorator("__and__", opname="bitwise AND", operator="&")
    __rand__ = _binaryop_decorator(
        "__rand__", opname="bitwise AND", operator="&", modifier=" (reversed) ")
    __iand__ = _binaryop_decorator(
        "__iand__", opname="bitwise AND", operator="&", modifier=" in-place ")

    __or__ = _binaryop_decorator("__or__", opname="bitwise OR", operator="|")
    __ror__ = _binaryop_decorator(
        "__ror__", opname="bitwise OR", operator="|", modifier=" (reversed) ")
    __ior__ = _binaryop_decorator(
        "__ior__", opname="bitwise OR", operator="|", modifier=" in-place ")

    __xor__ = _binaryop_decorator("__xor__", opname="bitwise XOR", operator="^")
    __rxor__ = _binaryop_decorator(
        "__rxor__", opname="bitwise XOR", operator="^", modifier=" (reversed) ")
    __ixor__ = _binaryop_decorator(
        "__ixor__", opname="bitwise XOR", operator="^", modifier=" in-place ")

    # data property
    def getData(self):
        """Default data property getter."""
        return self._data

    def setData(self, value):
        """Default data property setter."""
        if self.readonly:
            raise ReadonlyException("Field is readonly.")
        self._data = value
        self.dispatch(value, valuetype="data")

    def delData(self):
        """Default data property deleter."""
        if self.readonly:
            raise ReadonlyException("Field is readonly.")
        self._data = None
        self.dispatch(None, valuetype="data")

    # field properties
    @property
    def name(self):
        """
        Field name.

        .. note::
            As the name is used in :class:`IndexableField` as a key,
            the name should be hashable.
        """
        return self._name

    @name.setter
    def name(self, value):
        """Set the field name."""
        self._name = value
        self.dispatch(value, valuetype="name")

    @name.deleter
    def name(self):
        """Set the field name to None (as field.name = None)."""
        self._name = None
        self.dispatch(None, valuetype="name")

    @property
    def description(self):
        """Field description."""
        return self._description

    @description.setter
    def description(self, value: str):
        """Set the field description."""
        self._description = value
        self.dispatch(value, valuetype="description")

    @description.deleter
    def description(self):
        """Set the field description to None (as field.description = None)."""
        self._description = None
        self.dispatch(None, valuetype="description")

    descr = description

    @property
    def attributes(self) -> dict:
        """
        Field extra attributes.

        .. versionadded:: 0.2.0
        """
        return {} if self._attributes is None else self._attributes

    @attributes.setter
    def attributes(self, value: dict):
        """Set the field attributes."""
        if value in (None, {}):
            value = None
        elif not isinstance(value, dict):
            raise TypeError(
                "Field attributes must be a dict or a subclass of it")
        self._attributes = value
        self.dispatch(self.attributes, valuetype="attributes")

    @attributes.deleter
    def attributes(self):
        """Set the field attributes to an empty dict
        (as field.attributes = {})."""
        self.attributes = None

    attrs = attributes

    # event properies and methods
    @property
    def listener(self):
        """
        Field listeners.

        To add a new listener just assign it to this property.
        """
        return self._listeners

    @listener.setter
    def listener(self, func):
        """Add a new listener to the event listeners."""
        if callable(func):
            self._listeners.append(func)
        else:
            raise TypeError(
                "Given object typed {} is not a callable object".format(
                    type(func).__name__))

    @listener.deleter
    def listener(self):
        """Clear all the listeners."""
        self._listeners = []

    def dispatch(self, value, valuetype: str = "data"):
        """
        Call each listener with given value and type of the value.

        The `value` parameter type depends on the `valuetype` parameter.
        Here are listed all documented values assumed by `valuetype`.

        data
            Value is a generic (or a specific type if the field is typed) object.

            .. seealso::
                :class:`~TypedField` for typed fields.

        name
            Value is generically a string,
            but can be also a number in some languages (ex. json).

        description
            Value should be a string or a byte-like object.

        attributes
            Value should be a dict-like object.

            .. versionadded:: 0.2.0

        The value parameter can be None, regardless the valuetype.

        .. warning::
            Valuetype parameter can assume undocumented values
            so you should not raise any exception if the valuetype is not recognized
        """
        for func in self.listener:
            func(value, valuetype)

    # copy utilities
    def copyto(self, field, copy_listeners: bool = False):
        """
        Copy field attributes to another field.

        :param Field field: destination field

        :param bool copy_listeners: if True, the listeners
                                    will be added to destination field

        .. versionadded:: 0.4.0
        """
        field.readonly = self.readonly
        field.name = self.name
        field.data = self.data
        field.description = self.description
        field.attributes = self.attributes
        if copy_listeners:
            field._listeners.extend(self.listener)  # pylint: disable=W0212

    def copyfrom(self, field, copy_listeners: bool = False):
        """
        Copy all the field attributes from another field.

        :param Field field: source field

        :param bool copy_listeners: if True, the source field listeners
                                    will be added to self.

        .. warning::
            This method can bypass the :attr:`~Field.readonly` attribute if changes.

        .. versionadded:: 0.4.0
        """
        self.readonly = field.readonly
        self.name = field.name
        self.data = field.data  # pylint: disable=E0237
        self.description = field.description
        self.attributes = field.attributes
        if copy_listeners:
            self._listeners.extend(field.listener)  # pylint: disable=W0212

    # extra methods
    def prettify(self,
                 indentation: int = 0,
                 indentation_str: str = " " * 4,
                 to_print: bool = False) -> str:
        r"""
        Create a formatted view of the field."

        :param int indentation: the identation level where print the field,
                                useful for recursive algorithms.

        :param str indentation_str: a string used for a single indentation level,
                                    usually can be "    " (4 spaces) or "\t"

        :param bool to_print: if True, this method output directly in the standard output,
                              using :func:`print`. Otherwise, it returns a string containing
                              the formatted field.

        .. versionadded:: 0.4.0
        """

        def _ind(_str):
            return indentation_str * indentation + _str

        if to_print:
            print(
                _ind("Field details:"),
                _ind("type:        {}".format(type(self).__name__)),
                _ind("name:        {}".format(self.name)),
                _ind("data:        {}".format(self.data)),
                _ind("description: {}".format(self.description)),
                _ind("readonly:    {}".format(self.readonly)),
                _ind("attributes:  {}".format(
                    os.linesep.join("{} => {}".format(key, val)
                                    for key, val in self.attributes.items()))),
                sep=os.linesep,
            )
        else:
            retstr = ""
            retstr += _ind("Field details:") + os.linesep
            retstr += _ind("type:        {}".format(
                type(self).__name__)) + os.linesep
            retstr += _ind("name:        {}".format(self.name)) + os.linesep
            retstr += _ind("data:        {}".format(self.data)) + os.linesep
            retstr += _ind("description: {}".format(self.descr)) + os.linesep
            retstr += _ind("readonly:    {}".format(self.readonly)) + os.linesep
            retstr += _ind("attributes:{}{}".format(
                os.linesep,
                os.linesep.join(
                    "{} => {}".format(key, val)
                    for key, val in self.attributes.items()))) + os.linesep
            return retstr


class SeparatedField(Field):
    """
    Save field separator as field attribute.

    This class is useful with no well-defined languages (such as etc)
    with a field structure like this: **NSD**;

    where:

    - N is name;
    - S is separator;
    - D is data.

    This class adds "separator" as a valuetype in the :class:`~Field` event dispatcher.
    """

    __slots__ = ("_separator",)

    def __init__(self, *args, separator: str = "", **kwargs):
        super().__init__(*args, **kwargs)
        self._separator = separator

    @property
    def separator(self):
        """Field separator."""
        return self._separator

    @separator.setter
    def separator(self, value):
        """Set the field separator."""
        self._separator = value
        self.dispatch(value, valuetype="separator")

    @separator.deleter
    def separator(self):
        """Set the field name to None (as field.separator = None)."""
        self._separator = None
        self.dispatch(None, valuetype="separator")

    sep = separator


class NameField(Field):
    """A field without the data attribute."""

    data = None


class DataField(Field):
    """A field without the name attribute."""

    def __init__(self,
                 data=None,
                 description: str = "",
                 attributes: dict = None,
                 readonly: bool = False):
        # remove the required name attribute
        super().__init__(
            "",
            data=data,
            description=description,
            attributes=attributes,
            readonly=readonly)


# indexable fields
@data_decorator
class IndexableField(Field):
    """Represents a mutable and indexable data type."""

    # Python primitives converters
    @classmethod
    def from_primitives(cls,
                        obj,
                        fieldtypes: dict = None,
                        root_type: type = None,
                        description: str = "",
                        readonly: bool = False,
                        **attributes) -> Field:
        """
        Create an :class:`~IndexableField` instance
        from Python primitives.

        .. versionadded:: 0.4.0
        """

        def _type_checker(fieldkey, fieldval) -> Field:
            """Check field type and encapsulate key and val into specific field instance."""
            try:
                # try direct association
                final_fieldtype = fieldtypes[type(fieldval)]

            except KeyError:
                # fallback to for loop
                for datatype, fieldtype in fieldtypes.items():
                    if isinstance(fieldval, datatype):
                        final_fieldtype = fieldtype
                        break
                else:
                    raise NotImplementedError(
                        "Unimplemented data type {} of {}".format(
                            type(fieldval), fieldval))
            if issubclass(final_fieldtype, IndexableField):
                fieldinst = cls.from_primitives(
                    fieldval,
                    root_type=final_fieldtype,
                    fieldtypes=fieldtypes,
                    description=description,
                    readonly=readonly,
                    **attributes)
                fieldinst.name = fieldkey
            else:
                fieldinst = final_fieldtype(
                    name=fieldkey,
                    data=fieldval,
                    description=description,
                    readonly=readonly,
                    **attributes)
            return fieldinst

        if fieldtypes is None:
            fieldtypes = cls._default_datatypes
        if root_type is None:
            root_type = cls

        if isinstance(obj, dict):
            rootfield = root_type(
                name=None,
                data={
                    key: _type_checker(key, value)
                    for key, value in obj.items()
                },
                description=description,
                readonly=readonly,
                **attributes)
        else:
            rootfield = root_type(
                name=None,
                data=[_type_checker(None, value) for value in obj],
                description=description,
                readonly=readonly,
                **attributes)
        return rootfield

    def to_primitives(self, use_name: bool = False) -> object:
        """
        Convert the field tree into Python primitives.

        :param bool use_name:
            If True, try to use use the field name as containter key,
            This works good for dict-like object, but fails on arrays,
            so a progressive int will be used instead.

        .. warning::
            This method does not do any type casting,
            it only extracts name and data from fields.

        .. versionadded:: 0.4.0
        """

        def _recursive_extractor(field: Field):
            datacopy = copy.copy(field.data)

            if isinstance(field, IndexableField):
                for key, val in field.iteritems():
                    oldkey = None
                    if use_name and val.name != key:
                        oldkey = key
                        key = val.name

                    extracted = _recursive_extractor(val)

                    try:
                        datacopy[key] = extracted
                    except TypeError:
                        datacopy[oldkey] = extracted
                    else:
                        if oldkey is not None:
                            del datacopy[oldkey]

            return datacopy

        return _recursive_extractor(self)

    # reimplement data
    def setData(self, value):
        """Check if the given data is iterable."""
        if hasattr(value, "__iter__") and hasattr(value, "__getitem__"):
            super().setData(value)
        else:
            raise TypeError("Given data typed {} is not iterable".format(
                type(value).__name__))

    # index operators
    def __getitem__(self, key):
        """Implement :code:`obj[key]`"""
        return self.data.__getitem__(key)

    def __setitem__(self, key, val):
        """Implement :code:`obj[key] = val`"""
        if isinstance(val, Field):
            return self.data.__setitem__(key, val)
        raise TypeError(
            "Given data '{}' isn't an instance or Field or NoneType.".format(
                val))

    def __delitem__(self, key):
        """Implement :code:`del obj[key]`"""
        return self.data.__delitem__(key)

    # comparison operators
    def __contains__(self, other) -> bool:
        """
        Check if the given field is contained (the 'in' operator)
        in the field data.

        :raises TypeError: If :obj:`~Field.data` does not support this operator.

        .. versionadded:: 0.2.0
        """
        return self._data in other.data

    # data iterations
    def __iter__(self) -> iter:
        """Iterate data."""
        return self.data.__iter__()

    def iteritems(self) -> iter:
        """
        Iterate data items.

        By default, this method yields pairs containing a count,
        which start from zero, and the yielded value, as enumerate does.

        Subclasses must implement this method if first key
        isn't zero or it isn't a number.

        .. versionadded:: 0.4.0
        """
        return enumerate(self)

    # data properties
    def __len__(self) -> int:
        """
        Return the length of data.

        :raises TypeError: If :obj:`~Field.data` does not support this operator.

        .. versionadded:: 0.2.0
        """
        return len(self._data)

    # child manipulation
    def add(self, field: Field):
        """
        Add a :class:`~Field` object.

        Subclasses must implement this method if adding
        requires a different manner to be done.

        :raises IndexError:
            If field name isn't a valid key.

        .. versionadded:: 0.4.0
        """
        self[field.name] = field

    def remove(self, field: Field):
        """
        Remove first occurrence of given :class:`~Field` object.
        By default, it removes the field by its name.

        Subclasses must implement this method if removing
        requires a different manner to be done.

        :raises KeyError:
            If given :class:`~Field` object is not found.

        .. versionadded:: 0.4.0
        """
        del self[field.name]

    # utils
    def prettify(self,
                 indentation: int = 0,
                 indentation_str: str = " " * 4,
                 to_print: bool = False) -> str:

        def _ind(_str):
            return indentation_str * indentation + _str

        if to_print:
            print(
                _ind("Field details:"),
                _ind("type:        {}".format(type(self).__name__)),
                _ind("name:        {}".format(self.name)),
                _ind("description: {}".format(self.description)),
                _ind("readonly:    {}".format(self.readonly)),
                _ind("attributes:  {}".format(
                    os.linesep.join("{} => {}".format(key, val)
                                    for key, val in self.attributes.items()))),
                _ind("Data elements:"),
                sep=os.linesep)
        else:
            retstr = ""
            retstr += _ind("Field details:") + os.linesep
            retstr += _ind("type:        {}".format(
                type(self).__name__)) + os.linesep
            retstr += _ind("name:        {}".format(self.name)) + os.linesep
            retstr += _ind("description: {}".format(self.descr)) + os.linesep
            retstr += _ind("readonly:    {}".format(self.readonly)) + os.linesep
            retstr += _ind("attributes:{}{}".format(
                os.linesep,
                os.linesep.join(
                    "{} => {}".format(key, val)
                    for key, val in self.attributes.items()))) + os.linesep
            retstr += _ind("Data elements:") + os.linesep

        for field in self:
            fieldstr = field.prettify(
                indentation + 1,
                indentation_str=indentation_str,
                to_print=to_print)
            if to_print:
                print()
            else:
                retstr += fieldstr + os.linesep
        if not to_print:
            return retstr

    def count(self) -> int:
        """
        Recursively count the number of :class:`~Field` objects, including itself.

        If there is no children, 1 is returned.
        """

        counter = 1
        for child in self:
            if isinstance(child, IndexableField):
                counter += child.count()
            else:
                counter += 1

        return counter


class NestedField(IndexableField):
    """Represents a structured data that must contain instances of :class:`~Field` only."""

    def iteritems(self, i: int = 0) -> iter:
        for value in self._data:
            if isinstance(value, NestedField):
                yield from value.iteritems(i)
            elif isinstance(value, Field):
                yield i, value
            else:
                # It's very difficult to raise that exception
                raise TypeError("Found unvalid object typed {}".format(
                    type(value).__name__))
            i += 1

    def __iter__(self) -> iter:
        """Iterate over all children fields."""
        for _, value in self.iteritems():
            if isinstance(value, NestedField):
                yield from value.__iter__()
            elif isinstance(value, Field):
                yield value
            else:
                # It's very difficult to raise that exception
                raise TypeError("Found unvalid object typed {}".format(
                    type(value).__name__))


class TypedField(type):
    """
    Factory class of typed fields.

    It creates typed class that wrap type controls in :obj:`~Field.data` setter and
    in the :meth:`~Field.__init__` method.

    The type of data can be passed by calling directly this
    class or, in a class declaration, by the **__TYPEOBJ__** constant;
    when both is missing, object will become the type of data, making
    type controls useless.

    .. note::
      This class does not give any type control to :obj:`Field.name` attribute.
    """

    def __new__(cls, name, bases=(Field,), attr=None, typeobj=None):
        """Add type checks to :meth:`~Field.__init__` and setData methods."""
        if attr is None:
            attr = {}
        if typeobj is None:
            # look for special variable __TYPEOBJ__
            typeobj = attr.get("__TYPEOBJ__", object)

        obj = type(name, bases, attr)

        obj.__init__ = TypedField.check_type(obj.__init__, typeobj)
        obj.setData = TypedField.check_type(
            obj.setData, typeobj, only_data=True)
        obj = data_decorator(obj)

        return obj

    @staticmethod
    def check_type(func: callable, typeobj, only_data=False):
        """Return a decorated method with the type checker."""

        if only_data:

            def wrapper(self, data: typeobj):
                if not isinstance(data, (typeobj, NoneType)):
                    raise TypeError(
                        "Data {} isn't an instance or {} or NoneType.".format(
                            data, typeobj.__name__))
                return func(self, data)  # pylint: disable=E1123

        else:

            def wrapper(self, *args, data: typeobj = None, **kwargs):
                if not isinstance(data, (typeobj, NoneType)):
                    raise TypeError(
                        "Data {} isn't an instance or {} or NoneType.".format(
                            data, typeobj.__name__))
                return func(self, *args, data=data, **kwargs)  # pylint: disable=E1123

        return wrapper


# factoried classes
class StringField(Field, metaclass=TypedField):
    """Represents a string field."""
    __TYPEOBJ__ = str


class IntField(Field, metaclass=TypedField):
    """Represents an integer field."""
    __TYPEOBJ__ = int


class FloatField(Field, metaclass=TypedField):
    """Represents a float field."""
    __TYPEOBJ__ = float


class BoolField(Field, metaclass=TypedField):
    """Represents a boolean field."""
    __TYPEOBJ__ = bool


class ArrayField(IndexableField, metaclass=TypedField):
    """Represents an array (:class:`list`) field."""
    __TYPEOBJ__ = list

    def add(self, field: Field):
        """Add a :class:`Field` using :meth:`list.append`."""
        if self._data is None:
            self._data = self.__TYPEOBJ__()
        self.data.append(field)

    def append(self, *args, **kwargs):
        """
        An alias for :code:`field.data.append()`.

        .. versionadded:: 0.2.0
        """
        self.data.append(*args, **kwargs)

    def insert(self, *args, **kwargs):
        """
        An alias for :code:`field.data.insert()`.

        .. versionadded:: 0.2.0
        """
        self.data.insert(*args, **kwargs)

    def index(self, *args, **kwargs):
        """
        An alias for :code:`field.data.index()`.

        .. versionadded:: 0.2.0
        """
        self.data.index(*args, **kwargs)

    def extend(self, *args, **kwargs):
        """
        An alias for :code:`field.data.extend()`.

        .. versionadded:: 0.2.0
        """
        self.data.extend(*args, **kwargs)

    def remove(self, field: Field):
        try:
            self.data.remove(field)
        except (ValueError, KeyError) as ex:
            raise KeyError(*ex.args)


class DictField(IndexableField, metaclass=TypedField):
    """Represents a dictionary-like field."""

    __TYPEOBJ__ = dict

    def add(self, field: Field):
        if self._data is None:
            self._data = self.__TYPEOBJ__()
        super().add(field)

    def items(self):
        """
        An alias for :code:`field.data.items()`.

        .. versionadded:: 0.2.0
        """
        return self.data.items()

    def keys(self):
        """
        An alias for :code:`field.data.keys()`.

        .. versionadded:: 0.2.0
        """
        return self.data.keys()

    def values(self):
        """
        An alias for :code:`field.data.values()`.

        .. versionadded:: 0.2.0
        """
        return self.data.values()

    __iter__ = lambda self: iter(self.values())
    """
    Iterate over values to be compared to single-element iterable.

    .. versionadded:: 0.2.0
    """

    iteritems = items


# mixed classes
class StringSeparatedField(StringField, SeparatedField):
    """Represents a string field with separator."""


Field._default_datatypes.update(  # pylint: disable=W0212
    OrderedDict([
        (str, StringField),
        (bool, BoolField),
        (int, IntField),
        (float, FloatField),
        ((list, tuple), ArrayField),
        (dict, DictField),
        (NoneType, NameField),
    ]))
