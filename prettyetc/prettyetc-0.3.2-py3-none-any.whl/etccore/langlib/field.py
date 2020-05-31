#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=====
Field
=====


This module contains all builtins field types.
All of these fields can be extended or joint together.
However user-defined fields must inhiterits at least
:class:`~Field` for basic types, or :class:`~IndexableField` for collections.

That's a summary of basic field types avaiable.

:class:`~Field`
-----------------------------------------
This is the base class for all fields in this module
This class is considered the smallest element of a configuration file.


:class:`~TypedField`
----------------------------------------------
This make type controls in given data,
raising an error if the given data has a wrong type.


:class:`~IndexableField`
--------------------------------------------------
This allow a field to have children of fields
The data of an :class:`~IndexableField` can be a list, a dict, or something else.

:class:`~NameField`
---------------------------------------------
This field has no data.
"""

__all__ = ("Field", "SeparatedField", "NameField", "DataField",
           "IndexableField", "NestedField", "TypedField", "StringField",
           "IntField", "FloatField", "BoolField", "ArrayField", "DictField",
           "StringSeparatedField", "ReadonlyException")


class ReadonlyException(Exception):
    """Raised when field is readonly."""


def data_decorator(cls: type):
    """Create data property from methods."""
    cls.data = property(
        fget=cls.getData,
        fset=cls.setData,
        fdel=cls.delData,
        doc="Handle data stored in field.")
    return cls


# simple fields
@data_decorator
class Field(object):
    """
    Basic representation of Field.

    It manages and preserve all required attributes of a generic field.

    It provides a simple event manager based on change of atributes;
    see the dispatch method for more informations.
    Setting a new listener is simple, you just assign the function to
    listener variable.

    .. code::

        def foo(value, valuetype):
            # whatever you want
        field.listener = foo
        print(field.listener)  # [<function foo at 0xnnnnnnnnnnnn>]

    However you can manipulate directly the listener value,
    but is unsafe because the listener property setter
    make validations in the given callable.

    .. versionchanged:: 0.2.0
        Added field attribute "attributes"
        Added data converters and operators

    .. seealso::
        :ref:`API glossary` for a detailed description about what is a
        field and a detailed description of its attributes.

    """

    __slots__ = ("_name", "_description", "_data", "_attributes", "readonly",
                 "_listeners")
    data = None

    def __init__(self,
                 name,
                 data=None,
                 description: str = "",
                 attributes: dict = None,
                 readonly: bool = False):
        super().__init__()
        self._name = name
        self._description = description
        self._data = data
        if attributes is None:
            attributes = {}
        if not isinstance(attributes, dict):
            raise TypeError(
                "Field attributes must be a dict or a subclass of it.")
        self._attributes = attributes
        self.readonly = readonly
        self._listeners = []

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
        Get data string representation.

        :raises ValueError: if data is not convertible to str.

        .. versionadded:: 0.2.0
        """
        return str(self._data)

    def __bool__(self) -> bool:
        """
        Get data as bool.

        :raises ValueError: if data is not convertible to bool.

        .. versionadded:: 0.2.0
        """
        return int(self._data)

    def __int__(self) -> int:
        """
        Get data as int.

        :raises ValueError: if data is not convertible to int.

        .. versionadded:: 0.2.0
        """
        return int(self._data)

    def __float__(self) -> float:
        """
        Get data as float.

        :raises ValueError: if data is not convertible to float.

        .. versionadded:: 0.2.0
        """
        return float(self._data)

    def __hash__(self) -> int:
        """
        Get data hash.

        :raises ValueError: if data is unhashable.

        .. versionadded:: 0.2.0
        """
        return hash(self._data)

    # comparison operators
    def __eq__(self, other) -> bool:
        """
        Check field (name and data) equality.

        :raises TypeError: if the data is not comparable.

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

        :raises TypeError: if the data is not comparable.

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

        :raises TypeError: if the data is not comparable.

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

        :raises TypeError: if the data is not comparable.

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

        :raises TypeError: if the data is not comparable.

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

    def dispatch(self, value, valuetype: str = "data"):
        """
        Call each listener with given value and type of value
        Each

        The value parameter type depends of valuetype parameter.

        data
            If valuetype is data, value is a generic python object,
            or a specific type if the field is typed.
            .. seealso::

                :class:`~prettyetc.etccore.langlib.TypedField`
                for typed fields.

        name
            If valuetype is name, value is generically a string,
            but can be also a number in some languages (ex. json).

        description
            If valuetype is description,
            value should be a string or a byte-like object.

        attributes
            If valuetype is attributes,
            value should be a string or a byte-like object.

            .. versionadded:: 0.2.0

        The value parameter can be None, regardless the valuetype.

        .. warning::
            Valuetype parameter can assume undocumented values
            so you should not raise any exception if the valuetype is not recognized
        """
        for func in self.listener:
            func(value, valuetype)

    # field properties
    @property
    def name(self):
        """Field name."""
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
        return self._attributes

    @attributes.setter
    def attributes(self, value: dict):
        """Set the field attributes."""
        if value is None:
            value = {}
        elif not isinstance(value, dict):
            raise TypeError(
                "Field attributes must be a dict or a subclass of it")
        self._attributes = value
        self.dispatch(value, valuetype="attributes")

    @attributes.deleter
    def attributes(self):
        """Set the field attributes to an empty dict
        (as field.attributes = {})."""
        self._attributes = {}
        self.dispatch({}, valuetype="attrs")

    attrs = attributes

    @property
    def listener(self):
        """
        Field listeners.

        To add a new listener
        simply assign it to this property.
        """
        return self._listeners

    @listener.setter
    def listener(self, func):
        """Add a new listener to the event dispatcher."""
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


class SeparatedField(Field):
    """
    Save field separator as field attribute.

    This class is useful with no well defined languages (such as etc)
    with a field structure like this: **NSD**;

    where:

    - N is name;
    - S is separator;
    - D is data.

    This class add "separator" as a new datatype in the event dispatcher.
    """

    __slots__ = ("_separator", )

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
    """A field that haven't the data attribute."""

    data = None


class DataField(Field):
    """A field that haven't the name attribute."""

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
    """Represents an indexable data types."""

    def setData(self, value):
        """Check if the given data is iterable."""
        if hasattr(value, "__iter__") and hasattr(value, "__getitem__"):
            super().setData(value)
            self.dispatch(value, valuetype="data")
        else:
            raise TypeError("Given data typed {} is not iterable".format(
                type(value).__name__))

    # index operators
    def __getitem__(self, key):
        """Implement obj["key"] (e.g. dict)."""
        return self.data.__getitem__(key)

    def __setitem__(self, key, val):
        """Implement obj["key"] = val (e.g. dict)."""
        if isinstance(val, Field):
            return self.data.__setitem__(key, val)
        raise TypeError(
            "Given data '{}' isn't an instance or Field or NoneType.".format(
                val))

    def __delitem__(self, key):
        """Implement del obj["key"] (e.g. dict)."""
        return self.data.__delitem__(key)

    def __iter__(self):
        """Iterate data."""
        return self.data.__iter__()

    # comparison operators
    def __contains__(self, other) -> bool:
        """
        Check if the given field is contained (the 'in' operator)
        in the field data.

        :raises TypeError: if the data does not support this operator.

        .. versionadded:: 0.2.0
        """
        return self._data in other.data

    # data properties
    def __len__(self) -> int:
        """
        Return the lenght of data.

        :raises TypeError: if the data does not support this operator.

        .. versionadded:: 0.2.0
        """
        return len(self._data)


class NestedField(IndexableField):
    """Represent a structured data that must contain instances of :class:`~Field`."""

    def __iter__(self):
        """Iterate over all children fields."""
        try:
            # try dict-like data with items method
            for _, value in self._data.items():
                if isinstance(value, NestedField):
                    yield from value.__iter__()
                elif isinstance(value, Field):
                    yield value
                else:
                    # It's very difficult to raise that exception
                    raise TypeError("Found unvalid object Typed {}".format(
                        type(value).__name__))
        except AttributeError:
            # fallback to standard iteration
            for value in self._data:
                if isinstance(value, NestedField):
                    yield from value.__iter__()
                elif isinstance(value, Field):
                    yield value
                else:
                    # It's very difficult to raise that exception
                    raise TypeError("Found unvalid object Typed {}".format(
                        type(value).__name__))


class TypedField(type):
    """
    Factory class of typed fields.

    It create typed class that wrap type controls in setting data and
    **__init__**.

    The type of data can be passed by calling directly this
    class or, in a class declaration, by the **__TYPEOBJ__** costant;
    when both is missing, object will become the type of data, making
    type controls useless.

    .. note::
      Field name hasn't type controls as the field data.
    """

    def __new__(cls, name, bases=(Field, ), attr=None, typeobj=None):
        """Add type checks to __init__ and setData methods."""
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
        """Check if data type is correct, otherwise tho."""

        if only_data:

            def wrapper(self, data: typeobj):
                if not isinstance(data, (typeobj, type(None))):
                    raise TypeError(
                        "Data {} isn't an instance or {} or NoneType.".format(
                            data, typeobj.__name__))
                return func(self, data)  # pylint: disable=E1123

        else:

            def wrapper(self, *args, data: typeobj = None, **kwargs):
                if not isinstance(data, (typeobj, type(None))):
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
    """Represents an array (list) field."""
    __TYPEOBJ__ = list

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


class DictField(IndexableField, metaclass=TypedField):
    """Represents a dict field."""
    __TYPEOBJ__ = dict

    def __iter__(self) -> iter:
        """
        Iterate over values to be compared to single-element iterable.

        .. versionadded:: 0.2.0
        """
        return self.values().__iter__()

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


# mixed classes
class StringSeparatedField(StringField, SeparatedField):
    """Represents a string field with separator."""
