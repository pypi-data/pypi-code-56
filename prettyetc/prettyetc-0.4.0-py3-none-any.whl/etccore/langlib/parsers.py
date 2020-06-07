#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This module contains the abstract base of every parser and some partial
implementations, including a dedicated exception.

.. seealso::
    :class:`~BaseParser` class for more information about creating parsers.

.. seealso::
    The guide: :ref:`How to develop a language parser plugin`

"""

import abc
import io
import traceback

from ..logger import ChildLoggerHelper, errhelper
from .field import ArrayField, DictField, Field, IndexableField, StringField
from .root import RootField

__all__ = ("BaseParser", "PrimitiveParser", "DictParser", "StringFieldParser",
           "BadInput", "FileMatcher", "ReadAllParser")


class BadInput(ChildLoggerHelper, Exception):
    """
    Raised when input is not a valid for parser.

    This exception contains some information (including the original exception)
    to help ui to show it for the end user.
    All the information are optionals, but, if you give more information,
    the ui error will become more useful.
    A default string representation with all the information can be found in
    :meth:`~prettyetc.core.langlib.parsers.BadInput.__repr__`.

    :param str filename: name of the file

    :param str langname: name of the language

    :param int line: line (or lines) of the error.
      If lines are more than 1,
      the parameter can be an arbitrary iterable,
      not just list or tuples.

    :param int column: column (or columns) of the error.
      If columns are more than 1,
      the parameter can be an arbitrary iterable,
      not just list or tuples.

    :param str incriminated_string: The incriminated string that cause the error.

        .. versionchanged:: 0.2.0
            Do not use this argument for say the reason,
            use the reason parameter.

    :param str reason:
        Describe the entity of the error.

        .. versionadded:: 0.2.0

    :param bool is_valid: a check if the file is in that language  (default: True)
    :param Exception original_exc: The original exception

    Parameters to use this exception as a standard exception (optional).

    :param tuple args: original `args` Exception parameter.
    :param bool repr_toargs: use the class representation for the `args` parameter.
      This flag override the given args parameter.

    .. warning::
        Do not abuse of the line and columns attributes,
        this exception class is made for handle 1 error in the input.
        If you want to report more than 1 error, if possible, made different errors
    """
    __slots__ = ("filename", "langname", "line", "column", "reason"
                 "incriminated_string", "is_valid", "original_exc", "args")
    loggername = "etccore.langlib.badinput"

    def __init__(  # pylint: disable=R0913
            self,
            filename: str = None,
            langname: str = None,
            reason: str = None,
            line: int = None,
            column: int = None,
            incriminated_string: str = None,
            is_valid: bool = True,
            original_exc: Exception = None,
            args: tuple = None,
            repr_toargs: bool = False):

        self.reason = reason
        self.filename = filename
        self.langname = langname
        self.line = line
        self.column = column
        self.incriminated_string = incriminated_string
        self.is_valid = is_valid
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
            header = "An error occurred while parsing something."
        else:
            header = "An error occurred while parsing{}{}\n".format(
                filename,
                langname,
            )

        # line
        if self.line is None:
            line = ""
        elif isinstance(self.line, int):
            line = "At line {}".format(self.line)
        elif isinstance(self.line, range):
            # the step value will be ignored
            line = "At lines {}-{}".format(
                self.line.start,
                self.line.stop,
            )
        elif hasattr(self.line, "__iter__"):
            # very unsafe, use range instead
            line = "At lines {}".format(", ".join(self.line))
        else:
            raise errhelper(
                TypeError("Unsupported data type for line"),
                self.logger,
                "An error occurred while formatting the exception",
            )

        # column
        if self.column is None:
            column = ""
        elif isinstance(self.column, int):
            column = "at column {}".format(self.column)
        elif isinstance(self.column, range):
            # the step value will be ignored
            column = "at column {}-{}".format(
                self.column.start,
                self.column.stop,
            )
        elif hasattr(self.column, "__iter__"):
            # very unsafe, use range instead
            column = "at column {}".format(", ".join(self.column))
        else:
            raise errhelper(
                TypeError("Unsupported data type for column"),
                self.logger,
                "An error occurred while formatting the exception",
            )

        body = ""
        if line:
            body = line
            if column:
                body += ", {}\n".format(column)
            else:
                body += "\n"
        elif column:
            body = column.capitalize() + "\n"

        incriminated_string = ""
        if self.incriminated_string is not None:
            incriminated_string = self.incriminated_string + "\n"
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

        return header + body + incriminated_string + reason + tbstring


class BaseParser(ChildLoggerHelper, abc.ABC):
    """
    Abstract base of language configuration parsers.

    This class represented a standardized way to parse
    some configuration language strings.

    In particular, the parsing process begins with an ASCII text string,
    or a stream containing that, some parsing will be done and the result must be a
    :class:`.RootField` (or its subclass) object that represents the given
    configuration text as a :class:`.Field` tree.

    .. seealso::
        The guide: :ref:`How to develop a language parser plugin`

    .. versionchanged:: 0.2.0
        Now this class inherits :class:`abc.ABC`
        and all the abstract methods are decorated
        with :func:`abc.abstractmethod`.
    """

    LANGUAGES = ()
    PREFIXES = ()
    SUFFIXES = ()
    loggername = "etccore.langlib.parser"

    @abc.abstractmethod
    def parse_field(self,
                    name,
                    data,
                    description: str = "",
                    readonly: bool = False,
                    **attributes):
        """
        Parse single field.

        It should be called by :meth:`BaseParser.parse_line` or :meth:`BaseParser.parse_string`.

        :raises NotImplementedError: If this method is not implemented.

        :raises TypeError: If the given data type is not supported.
            This exception should be handled by caller.

            .. danger::
                This exception is not handled by standard parser callers
                (e.g. :class:`.ConfigStream`).
                Therefore, propagating this exception outside the parser
                can cause crash or unexpected behaviours.
        """
        raise NotImplementedError("Method parse_field must be implemented.")

    @abc.abstractmethod
    def parse_line(self, line: str):
        """
        Parse single line.

        This abstract method is the default way for parsing streams.
        See deprecation note for more information about why you shouldn't use this.

        :raises NotImplementedError: If this method is not implemented.

        .. deprecated:: 0.4.0
            This method exists since first version of prettyetc,
            but it is never used in the whole library, and only the etc parser implements it.
            So we decided to deprecate this method in favor of :meth:`BaseParser.parse_string`.

            However, this method continues to be the default way to parsing until
            this method will be removed.
        """
        raise NotImplementedError("Method parse_line must be implemented")

    @abc.abstractmethod
    def parse_string(self, string: str):
        """
        Parse a configuration as string.

        This abstract method is optional for parsing, but if you would use it,
        you should change parse_file before, or use DictField if is good for
        what you are doing.

        :raises NotImplementedError: If this method is not implemented.
        """
        raise NotImplementedError("Method parse_string must be implemented")

    def parse_file(self, stream: open, **kwargs) -> RootField:
        """
        Read a file; by default it read single lines.

        :raises BadInput: If an error occurred while
                          parsing the content of the stream.

        :raises IOError: If an error occurred while reading
                         the stream or the stream is not a valid readable stream.
        """
        fields = []
        i = None
        if isinstance(stream, io.TextIOWrapper) and stream.readable():
            try:
                for i, line in enumerate(stream):
                    fields.append(self.parse_line(line, **kwargs))

            except UnicodeDecodeError as ex:
                raise BadInput(
                    filename=stream.name,
                    # assuming that is a binary data, so there are no lines.
                    column=range(ex.start, ex.end),
                    line=i,
                    reason=ex.reason,
                    langname=self.LANGUAGES[0],
                    original_exc=ex)

            except BadInput as ex:
                ex.filename = stream.name
                ex.line = i
                raise ex
            root = RootField(
                "root",
                langname=self.LANGUAGES[0],
                data=fields,
                name=stream.name)
            return root
        raise IOError("Given stream isn't readable.")


class ReadAllParser(BaseParser):  # pylint: disable=W0223
    """
    Change file reading way.
    In particular, this class change the
    :meth:`~BaseParser.parse_file` in order to read the whole stream into a single string,
    that will be passed to :meth:`~BaseParser.parse_string`

    .. versionadded:: 0.4.0
    """

    def parse_file(self, stream: open, **kwargs) -> RootField:
        """Read all content of a file-like object, must be readable."""
        if isinstance(stream, io.TextIOWrapper) and stream.readable():
            try:
                root = self.parse_string(stream.read(), **kwargs)
                root.name = stream.name

            except UnicodeDecodeError as ex:
                raise BadInput(
                    filename=stream.name,
                    # assuming that is a binary data, so there are no lines.
                    column=range(ex.start, ex.end),
                    reason=ex.reason,
                    langname=self.LANGUAGES[0],
                    original_exc=ex)
            except BadInput as ex:
                ex.filename = stream.name
                raise ex
            return root
        raise IOError("Given stream isn't readable.")


class PrimitiveParser(BaseParser):  # pylint: disable=W0223
    """
    A partial implementation of BaseParser for parse python primitives to fields.

    .. deprecated:: 0.4.0
        Use :meth:`.IndexableField.from_primitives` instead.
    """

    def parse_field(self,
                    name,
                    data,
                    description: str = "",
                    readonly=False,
                    **attributes) -> Field:
        # if data is None:
        #     return NameField(
        #         name,
        #         description=description,
        #         readonly=readonly,
        #         attributes=attributes)
        # if isinstance(data, bool):
        #     return BoolField(
        #         name,
        #         data=data,
        #         description=description,
        #         readonly=readonly,
        #         attributes=attributes)
        #
        # if isinstance(data, int):
        #     return IntField(
        #         name,
        #         data=data,
        #         description=description,
        #         readonly=readonly,
        #         attributes=attributes)
        #
        # if isinstance(data, float):
        #     return FloatField(
        #         name,
        #         data=data,
        #         description=description,
        #         readonly=readonly,
        #         attributes=attributes)
        #
        # if isinstance(data, str):
        #     return StringField(
        #         name,
        #         data=data,
        #         description=description,
        #         readonly=readonly,
        #         attributes=attributes)
        #
        # if isinstance(data, (list, tuple)):
        #     return ArrayField(
        #         name,
        #         data=[self.parse_field(None, val) for val in data],
        #         description=description,
        #         readonly=readonly,
        #         attributes=attributes)
        #
        #     # return ArrayField(name, data=data, description=description)
        #
        # if isinstance(data, dict):
        #     return DictField(
        #         name,
        #         data={
        #             key: self.parse_field(key, val)
        #             for key, val in data.items()
        #         },
        #         description=description,
        #         readonly=readonly,
        #         attributes=attributes)
        try:
            # compatibility code
            if isinstance(data, dict):
                root_type = DictField
            elif isinstance(data, (list, tuple)):
                root_type = ArrayField
            else:
                root_type = None

            field = IndexableField.from_primitives(
                data,
                root_type=root_type,
                description=description,
                readonly=readonly,
                **attributes)
            field.name = name
            return field
        except NotImplementedError as ex:
            raise errhelper(ex, self.logger)


class DictParser(PrimitiveParser, ReadAllParser):  # pylint: disable=W0223
    """
    A partial implementation of BaseParser for dict-like configuration
    languages.

    It implements parsing of fields and a redefinition of parse_file to
    using parse_string instead of parse_line.
    This parser is good for languages that can be represented in a dict,
    such as JSON, YAML and INI-like files.

    .. warning::
        This implementation process only fields as dicts, array-like objects and primitive types.
        Nor comments, neither structured types are supported.

    .. deprecated:: 0.4.0
        Use :class:`~ReadAllParser` class instead and use
        :meth:`.IndexableField.from_primitives`
        for field processing.
    """


class StringFieldParser(BaseParser):  # pylint: disable=W0223
    """Partial implementation for string-only configuration languages."""

    def parse_field(self,
                    name,
                    data,
                    description: str = "",
                    readonly: bool = False,
                    **attributes) -> StringField:
        return StringField(
            name,
            data=data,
            description=description,
            attributes=attributes,
            readonly=readonly)


# parsing related stuffs
class FileMatcher(ChildLoggerHelper):
    """
    Find properly class for parsing or writing.

    It provides a communication layer between plugin manager and what
    manages files (often the frontend).

    .. deprecated:: 0.4.0
        Use :class:`~prettyetc.etccore.confmgr.ConfigStream` instead.
    """

    loggername = "etccore.langlib.parser.matcher"

    def __init__(self, pluginmgr):
        super().__init__()
        self.mgr = pluginmgr

    def get_language(self, lang: str, type_: str = "parser") -> BaseParser:
        """
        Get first occurrence of given language, searched in plugin lists.

        If no plugin is found, it will return None.
        """
        if type_ == "parser":
            for parser in self.mgr.loaded_parsers.values():
                if lang in parser.LANGUAGES:
                    return parser

        # elif type_ == "writer":
        #     for writer in self.mgr.loaded_writers.values():
        #         if lang in writer.LANGUAGES:
        #             return writer

        return None

    def match_filename(self, path: str) -> BaseParser:
        """
        Find the properly parser by given path to file.

        This method in particular locking for file names, especially
        suffixes, if no parser has been found, call the try_parser
        method.

        .. warning::
            This method doesn't guarantee that the given file is valid.
        """
        for parser in self.mgr.loaded_parsers.values():
            for suffix in parser.SUFFIXES:
                if path.endswith(suffix):
                    self.logger.debug(
                        "Found parser %s for %s file, using match_filename.",
                        parser.__name__, path)
                    return parser
            for prefix in parser.PREFIXES:
                if path.startswith(prefix):
                    self.logger.debug(
                        "Found parser %s for %s file, using match_filename.",
                        parser.__name__, path)
                    return parser
        return None

    def try_parser(self, file: open,
                   hint: BaseParser = None) -> (BaseParser, RootField):
        """Try to parse the file, if parsing is successful, returns the
        parser and the parsed content."""
        parsers = list(self.mgr.loaded_parsers.values())
        if hint is not None and issubclass(hint, BaseParser):
            try:
                parser_inst = hint()
                parsed = parser_inst.parse_file(file)

            except BadInput:
                self.logger.debug("Parser %s isn't valid for that file.",
                                  hint.__name__)
            except IOError as ex:
                self.logger.warning(
                    "An error occurred while reading the file.\nReason:",
                    exc_info=ex)

                raise BadInput(
                    filename=ex.filename,
                    is_valid=False,
                    reason="An error occurred while reading the file.",
                    original_exc=ex)

            else:
                return hint, parsed
            file.seek(0)
            parsers.remove(hint)

        for parser in parsers:
            try:
                temp_parser = parser()
                parsed = temp_parser.parse_file(file)

            except BadInput:
                self.logger.debug("Parser %s isn't valid for that file.",
                                  parser.__name__)
            except IOError as ex:
                self.logger.warning(
                    "An error occurred while reading the file.\nReason:",
                    exc_info=ex)

                raise BadInput(
                    filename=ex.filename,
                    is_valid=False,
                    reason="An error occurred while reading the file.",
                    original_exc=ex)

            else:
                return parser, parsed
            file.seek(0)

        return None, None
