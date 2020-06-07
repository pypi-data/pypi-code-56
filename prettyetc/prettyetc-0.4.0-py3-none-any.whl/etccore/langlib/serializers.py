#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This module contains the abstract base of every serializer and some partial
implementations, including a dedicated exception.

.. seealso::
    :class:`~BaseSerializer` class for more information about serializer creation.

.. seealso::
    The guide: :ref:`How to develop a language serializer plugin`

.. versionadded:: 0.4.0

"""
import abc
import io
import traceback
from collections import namedtuple

from ..logger import ChildLoggerHelper, errhelper
from .field import ArrayField, DictField, Field, IndexableField
from .root import RootField

__all__ = ("BaseSerializer", "SerializeFailed")


class SerializeFailed(Exception):
    """
    Raised when a serialize operation fails.

    :param str filename: name of the file.
    :param str langname: name of the language.

    :param str reason:
        Describes the entity of the error.

    :param Exception original_exc: The original exception.

    :param tuple args: original args Exception parameter.
    :param bool repr_toargs: use the class representation for the args parameter.
      This flag override the given args parameter.

    .. versionadded:: 0.4.0
    """

    __slots__ = (
        "filename",
        "langname",
        "reason",
        "original_exc",
        "args",
    )
    loggername = "etccore.langlib.writefailed"

    def __init__(self,
                 filename: str = None,
                 langname: str = None,
                 reason: str = None,
                 original_exc: Exception = None,
                 args: tuple = None,
                 repr_toargs: bool = False):

        self.reason = reason
        self.filename = filename
        self.langname = langname
        self.original_exc = original_exc

        if repr_toargs:
            args = (repr(self),)
        else:
            if original_exc:
                args = ("Original traceback: {}".format(self.original_exc),)
            elif args is None:
                args = ()

        super().__init__(*args)

    def __repr__(  # pylint: disable=R0912
            self,
            add_tb: bool = False,
            original_repr: bool = False) -> str:

        # header
        if original_repr:
            return super().__repr__()
        filename = "" if self.filename is None else " the file {}".format(
            self.filename)
        langname = "" if self.langname is None else ", using the language {}".format(
            self.langname)
        if filename + langname == "":
            header = "Error while parsing something."
        else:
            header = "Error while parsing{}{}\n".format(
                filename,
                langname,
            )

        tbstring = ""
        reason = ""
        if self.reason is not None:
            reason = "Reason: " + self.reason + "\n"
        if add_tb and self.original_exc is not None:
            tbstring = "Original traceback was:\n{}".format(" ".join(
                traceback.format_exception(
                    type(self.original_exc),
                    self.original_exc,
                    self.original_exc.__traceback__,
                )))

        return header + reason + tbstring


class BaseSerializer(ChildLoggerHelper, abc.ABC):
    """
    Abstract base of language configuration serializers.

    This class represented a standardized way to serialize
    a :class:`.RootField` into a configuration language string.

    In particular, the serializing process with a root field,
    and a stream to write in,
    some serializes will be done and the result must be a
    syntactically correct configuration string.

    Serializer objects can be configured through pre-defined
    parameters, that are saved into the settings attribute (a dictionary).
    Language specific implementations of this class should not use all keys
    in settings because the language itself or the required 3rd party library
    doesn't support it.

    :param bool silent_discard:
        If True, the serializer doesn't raise a :exc:`~SerializeFailed` exception
        when some fields can't be serialized, but they will be discarded.
        This flag does not suppress errors when nothing can be written.

    :param bool beautify:
        If True, fields are dumped in a pretty-printed format
        This parameter can do nothing if language has no distinction
        between normal and pretty-printed strings.

    :param str indent:
        Default value is a four-spaces string.
        Some languages use the length of the string, ignoring its content.

    :param other:
        All the language specific settings.
        The caller should know what these parameters mean.

    .. seealso::
        The guide: :ref:`How to develop a language serializer plugin`

    .. versionadded:: 0.4.0
    """

    LANGUAGES = ()
    STANDARD_EXTENSION = ""
    loggername = "etccore.langlib.writer"
    _SETTINGS_TUPLE = namedtuple("_BaseSerializerSettings", (
        "silent_discard",
        "beautify",
        "indent",
        "other",
    ))

    @classmethod
    def normalize_field(cls, field: Field,
                        mapping_fieldtype: type = DictField) -> Field:
        """Make the field prettier and optimized for serializing."""
        if isinstance(field, ArrayField):
            keys = set()
            for key, child in field.iteritems():
                if child.name is not None and key != child.name:
                    keys.add(key)
            if keys:
                for key, child in field.iteritems():
                    # prepare child field to be copied
                    # create the new field
                    newfield = mapping_fieldtype(
                        None,
                        data={child.name: child},
                        description=child.description,
                        attributes=child.attributes,
                        readonly=child.readonly)

                    # replace the child field with the new one
                    field[key] = newfield
                    # remove duplicated description and attrs in child
                    child.description = ""
                    child.attributes = {}

        if isinstance(field, IndexableField):
            # for key, child in field:
            #     field[key] = cls.normalize_field(child)
            for child in field:
                cls.normalize_field(child, mapping_fieldtype=mapping_fieldtype)

        # if isinstance(field, Field):
        #     pass
        return field

    def __init__(self,
                 silent_discard: bool = False,
                 beautify: bool = False,
                 indent: str = "    ",
                 **other):
        super().__init__()
        self.settings = BaseSerializer._SETTINGS_TUPLE(
            silent_discard,
            beautify,
            indent,
            other,
        )

    @abc.abstractmethod
    def serialize_field(self, field: Field) -> str:
        """
        Serialize single field.

        It's had to be called by :meth:`.BaseSerializer.serialize_string`.

        :raises NotImplementedError: If this method is not implemented.

        :raises TypeError: If the given field type is not supported.
            This exception should be handled by the caller.

            .. danger::
                This exception is not handled by standard serialize callers
                (e.g. :class:`.ConfigStream`).
                Therefore, propagating this exception outside the serializer
                can cause crashes or unexpected behaviours.
        """
        raise NotImplementedError("Method serialize_field must be implemented.")

    @abc.abstractmethod
    def serialize_string(self,
                         field: IndexableField,
                         stream: io.IOBase = None,
                         **_) -> str:
        """
        Create a configuration string from given field.

        Dumping of the stream can be done in 2 ways:

        - Dumping the content into a string that will be returned (required)
        - Writing into the given stream. (optional)

        :param prettyetc.etccore.langlib.field.IndexableField field:
            The field to dump

        :param io.IOBase stream:
            The stream where language-formatted string will be written.

            The implementation of this parameter is optional, but helps
            some library that doesn't support serializing to string or
            prefer streams due to performance issues.

            If the stream is given and you want to use that, you shouldn't
            return what you are written but None (no return).

        :raises NotImplementedError: If this method is not implemented.

        :raises SerializeFailed: If field and its content can't be dumped into
                                     a language string.
        """
        raise NotImplementedError("Method serialize_string must be implemented")

    def serialize_file(self, rootfield: RootField, stream: io.IOBase, **_):
        """
        Serialize to stream, by default it writes the given content of
        :meth:`~BaseSerializer.serialize_string`.

        :raises IOError: If an error occurred while reading
                         the stream or the stream is not a valid readable stream.

        :raises SerializeFailed: If given rootfield and its content can't be dumped into
                                     the language-formatted file.
        """
        if isinstance(stream, io.IOBase) and stream.writable():
            try:
                content = self.serialize_string(rootfield, stream=stream, **_)
            except SerializeFailed as ex:
                if hasattr(stream, "name"):
                    ex.filename = stream.name
                raise ex

            try:
                if content is not None:
                    stream.write(content)
            except IOError as ex:
                errhelper(ex, self.logger)
            else:
                return
        raise IOError("Given stream isn't writable.")
