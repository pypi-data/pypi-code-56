#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
==============================
Configuration Language library
==============================

Core stuffs for managing configuration data.

The whole structure is based on fields, objects that contain a name,
some data and an optional description.

That's a summary of basic field types.


Field
-----
This is the base class for all fields in this module
This class is considered the smallest element of a configuration file
It is composed by a name, the data, the description and some other fields.
See class documentation for more informations.


TypedField
----------
This make type controls in given data,
raising an error if the given data has a wrong type.


IndexableField
--------------
This allow a field to have children of fields
The data of an IndexableField can be a list, a dict, or something else.

NameField
---------
This field has no data, only name.

Content:
--------

- Field
- TypedField
- IndexableField
- NameField
- StringField (factoried)
- BoolField (factoried)
- IntField (factoried)
- FloatField (factoried)
- ArrayField (factoried)
- DictField (factoried)
- ReadonlyException

"""

__all__ = ("Field", "SeparatedField", "NameField", "DataField",
           "IndexableField", "NestedField", "RootField", "TypedField",
           "StringField", "IntField", "FloatField", "BoolField", "ArrayField",
           "DictField", "StringSeparatedField", "ReadonlyException")


class ReadonlyException(Exception):
    """Raised when field is readonly."""


def data_decorator(cls: type):
    """Create data property."""
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

    It manages and preserve all required attributes of a generic field,
    name, data, description and if can the data can be override or not (readonly).

    It provides a simple event manager based on change of atributes;
    see the dispatch method for more informations.
    Setting a new listener is simple, you just assign the function to
    listener variable.

    .. code:: python

        def foo(value, valuetype):
            # whatever you want
        field.listener = foo
        print(field.listener)  # [<function foo at 0xnnnnnnnnnnnn>]

    However you can manipulate directly the listener value, but the
    property setter make properly controls in the given callable.
    """

    __slots__ = ("_name", "_description", "_data", "readonly", "_listeners")
    data = None

    def __init__(self,
                 name,
                 data=None,
                 description: str = "",
                 readonly: bool = False):
        super().__init__()
        self._name = name
        self._description = description
        self._data = data
        self.readonly = readonly
        self._listeners = []

    def __repr__(self):
        """Generate object representation."""
        if self.description:
            desc = " {} ".format(self.description)
        else:
            desc = ""
        return "<{} {}={} {}{}>".format(
            type(self).__name__, self.name, self._data, desc, " readonly"
            if self.readonly else "")

    def __str__(self):
        """Return data string representation."""
        return str(self._data)

    def __eq__(self, other):
        """Compare fields."""
        if isinstance(other, Field):
            if self._name == other.name and \
               self._data == other.data:
                # also description can be compared
                # self.description == other.description and \
                return True
        return False

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
        Call each listener with given value and type of value.

        The value parameter type depends of valuetype parameter.

        - If valuetype is data, value is a generic python object, or a
          specific type if the field is typed.

        - If valuetype is name, value is generically a string,
          but can be also a number in some languages (ex. json).

        - If valuetype is description, value should be a string or a byte-like object.

        The value parameter can be None, regardless the valuetype.
        """
        for func in self.listener:
            func(value, valuetype)

    @property
    def name(self):
        """Get the field name."""
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
        """Get the field description."""
        return self._description

    @description.setter
    def description(self, value: str):
        """Set the field description."""
        self._description = value
        self.dispatch(value, valuetype="description")

    @description.deleter
    def description(self):
        """Set the field description to None (as field.description = None)."""
        self.description = None
        self.dispatch(None, valuetype="description")

    @property
    def listener(self):
        """The listener property getter."""
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

    def __init__(self, *args, separator="", **kwargs):
        super().__init__(*args, **kwargs)
        self._separator = separator

    @property
    def separator(self):
        """Get the field separator."""
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


class NameField(Field):
    """A field that haven't the data attribute."""

    data = None


class DataField(Field):
    """A field that haven't the name attribute."""

    def __init__(self,
                 data=None,
                 description: str = "",
                 readonly: bool = False):
        # remove the required name attribute
        super().__init__(
            "", data=data, description=description, readonly=readonly)


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

    def __getitem__(self, key):
        """Implement obj["key"] (e.g. dict)."""
        self.data.__getitem__(key)

    def __setitem__(self, key, val):
        """Implement obj["key"] = val (e.g. dict)."""
        if isinstance(val, Field):
            self.data.__setitem__(key, val)
        raise TypeError(
            "Given data '{}' isn't an instance or Field or NoneType.".format(
                val))

    def __delitem__(self, key):
        """Implement del obj["key"] (e.g. dict)."""
        self.data.__delattr__(key)

    def __iter__(self):
        """Iterate data."""
        return self.data.__iter__()


class NestedField(IndexableField):
    """Represent a structured data that must contain instances of Field."""

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


class RootField(NestedField):
    """
    Represent the root field.

    The root field can be compared to a config file.
    """

    def __init__(self, *args, typeconf="", metadata=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.typeconf = typeconf
        if metadata is None:
            metadata = {}
        else:
            self.metadata = metadata


class TypedField(type):
    """
    Factory class of typed fields.

    It create typed class that wrap type controls in setting data and
    **__init__**.

    The type of data can be passed by calling directly this
    class or, in a class declaration, by the **__TYPEOBJ__** costant; when
    both is missing, object will become the type of data.

    .. warning::
      Field name hasn't type controls as the field data.
    """

    def __new__(cls, name, bases=(Field, ), attr=None, typeobj=None):
        """Add type checks to __init__ and setData methods."""
        if attr is None:
            attr = {}
        if typeobj is None:
            # look for special variable __TYPEOBJ__
            # if is missing, object class is used instead
            # so type controls is useless.
            typeobj = attr.get("__TYPEOBJ__", object)
        attr["__init__"] = TypedField.check_type(attr["__init__"], typeobj)
        attr["setData"] = TypedField.check_type(attr["setData"], typeobj)
        obj = type(name, bases, attr)
        obj = data_decorator(obj)

        return obj

    @staticmethod
    def check_type(func, typeobj):
        """Check if data type is correct."""

        def wrapper(self, *args, data=None, **kwargs):
            if not isinstance(data, typeobj) or not isinstance(
                    kwargs.get("data"), (typeobj, type(None))):
                raise TypeError(
                    "Data {} isn't an instance or {} or NoneType.".format(
                        data, typeobj.__name__))
            func(self, *args, **kwargs)

        return wrapper


# factoried classes


class StringField(Field):
    """Represents a string field."""
    __metaclass__ = TypedField
    __TYPEOBJ__ = str


class IntField(Field):
    """Represents an integer field."""
    __metaclass__ = TypedField
    __TYPEOBJ__ = int


class FloatField(Field):
    """Represents a float field."""
    __metaclass__ = TypedField
    __TYPEOBJ__ = float


class BoolField(Field):
    """Represents a boolean field."""
    __metaclass__ = TypedField
    __TYPEOBJ__ = bool


class ArrayField(IndexableField):
    """Represents an array (list) field."""
    __metaclass__ = TypedField
    __TYPEOBJ__ = list


class DictField(IndexableField):
    """Represents a dict field."""
    __metaclass__ = TypedField
    __TYPEOBJ__ = dict


# mixed classes


class StringSeparatedField(StringField, SeparatedField):
    """Represents a string field with separator."""
