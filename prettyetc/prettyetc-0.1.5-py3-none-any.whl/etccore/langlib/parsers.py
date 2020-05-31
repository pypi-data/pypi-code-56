#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

=======
Parsers
=======

This module contains the abstract base of every parser and some partial
implementations, and some other stuff for error handling and file matching.
See classes documentation for more informations about single component.

Content

- BaseParser (abstract)
- DictParser (abstract)
- StringFieldParser (abstract)
- FileMatcher
- BadInput (Exception)


---------------------------------
Instruction to implement a parser
---------------------------------

Steps
`````
1. create a Python file

2. Add a subclass BaseParser (or a subclass of BaseParser)

That subclass contains the implementations of your plugin parser

3. Add the metadata informations:

  - **loggername**
      Set the logger name in logging syntax
      (if you want to use integrated logger).

  - **LANGUAGES**
       A tuple of languages that the parser provides.

  - **PREFIXES**
       A tuple of prefixes that the acceptable files can have,
       used by the file matcher.

  - **SUFFIXES**
       A tuple of suffixes that the acceptable files can have,
       used by the file matcher.

4. Implements the abstract methods

  You can parse a config using in differents way.

  - by parsing the whole file as a string

   (the common situation if you use an external library).

  - by parsing each line of a file (default way).
  - by parsing file using chunks of string.

   (probably no one use this way)

  This is the abstract methods list.


  - :meth:`~etccore.langlib.parsers.BaseParser.parse_field`
      A recursive method that create fields by given name,
      data and description (if avaiable).

      The data can be a collection of fields that children
      should be converted to fields.

      See etccore.baselang fields definitions for more informations.

  - :meth:`~etccore.langlib.parsers.BaseParser.parse_line`
      Parse a line of config
  - :meth:`~etccore.langlib.parsers.BaseParser.parse_string`
      Parse a string of config
  - :meth:`~etccore.langlib.parsers.BaseParser.parse_file`
      Parse a file-like stream of config,
      the given should have implemented the name attribute and the read method.

5. Creating the root field

  The root field must be an instance of RootField
  that contains all the valid, and processed, fields in the config.

"""

import io
import sys
import traceback

from prettyetc.etccore.logger import ChildLoggerHelper, errhelper

from . import (ArrayField, BoolField, DictField, FloatField, IntField,
               RootField, StringField)

__all__ = ("BaseParser", "DictParser", "StringFieldParser", "BadInput")


class BadInput(ChildLoggerHelper, Exception):
    """
    Raised when input is not a valid for parser.

    This exception contains some information (including the original exception)
    to help ui to show it for the end user.
    All the informations are optionals, but,
    if you give more informations, the ui error will become more useful.

    :param str filename: name of the file
    :param str langname: name of the language
    :param int line: line (or lines) of the error
    :param int column: column (or columns) of the error
    :param str incriminated_string: the incriminated piece of the config
    :param bool is_valid: a check if the file is in that language  (default: True)
    :param Exception original_exc: The original exception

    Params to use this exception as a standard exception (optional).
    :param tuple args: original args Exception parameter.
    :param bool repr_toargs: use the class representation for the args parameter.
                             this flag override the given args parameter.

    .. note::
        Line and column attribute (if there are more than one) can be expressed as an arbitrary iterable
        (ex. range), not just lists.

    .. warning::
        Do not abuse of the line and columns attributes,
        this exception class is made for handle 1 error in the input.
        If you want to report more than 1 error, if possible, made different errors
    """
    __slots__ = ("filename", "langname", "line", "column",
                 "incriminated_string", "is_valid", "original_exc", "args")
    loggername = "langlib.badinput"

    def __init__(self,
                 filename: str = None,
                 langname: str = None,
                 line: int = None,
                 column: int = None,
                 incriminated_string: str = None,
                 is_valid: bool = True,
                 original_exc: Exception = None,
                 args: tuple = None,
                 repr_toargs: bool = False):

        self.filename = filename
        self.langname = langname
        self.line = line
        self.column = column
        self.incriminated_string = incriminated_string
        self.is_valid = is_valid
        self.original_exc = original_exc

        if repr_toargs:
            args = (repr(self), )
        else:
            if original_exc:
                args = ("Original traceback: {}".format(self.original_exc), )
            elif args is None:
                args = ()
            else:
                args = args

        super().__init__(*args)

    def __repr__(  # pylint: disable=R0912
            self,
            add_tb: bool = False,
            original_repr: bool = False) -> str:
        # header
        if original_repr:
            return super().__repr__()
        filename = "" if self.filename is None else "the file {}".format(
            self.filename)
        langname = "" if self.langname is None else ", using the language {}".format(
            self.langname)
        if filename + langname == "":
            header = "Error while parsing something."
        else:
            header = "Error while parsing {}{}\n".format(filename, langname)

        # line
        if self.line is None:
            line = ""
        elif isinstance(self.line, int):
            line = "At line {}".format(self.line)
        elif isinstance(self.line, range):
            # the step value will be ignored
            line = "At lines {}-{}".format(self.line.start, self.line.stop)
        elif hasattr(self.line, "__iter__"):
            # very unsafe, use range instead
            line = "At lines {}".format(", ".join(self.line))
        else:
            raise errhelper(
                TypeError("Unsupported data type for line"), self.logger,
                "An error occurred while formatting the exception")

        # column
        if self.column is None:
            column = ""
        elif isinstance(self.column, int):
            column = "at column {}".format(self.column)
        elif isinstance(self.column, range):
            # the step value will be ignored
            column = "at column {}-{}".format(self.column.start,
                                              self.column.stop)
        elif hasattr(self.column, "__iter__"):
            # very unsafe, use range instead
            column = "at column {}".format(", ".join(self.column))
        else:
            raise errhelper(
                TypeError("Unsupported data type for column"), self.logger,
                "An error occurred while formatting the exception")

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
        if add_tb and self.original_exc is not None:
            tbstring = "Original traceback was:\n{}".format(" ".join(
                traceback.format_exception(
                    type(self.original_exc), self.original_exc,
                    self.original_exc.__traceback__)))

        return header + body + incriminated_string + tbstring


class BaseParser(ChildLoggerHelper):
    """
    Abstract base of configuration parsers.

    See module documentation for a quick start.
    """

    LANGUAGES = ()
    PREFIXES = ()
    SUFFIXES = ()
    loggername = "langlib.parser"

    if sys.version_info.minor >= 6:

        def __init_subclass__(cls, check_abstract: bool = True, **kwargs):
            """Check if abstract method is implemented."""
            # NOTE: logger require an instanced LoggerCreator object
            # that is not avaiable in class definitions
            # so root logger is logging.root
            # childlogger_helper(cls.loggername, cls)
            # cls.logger.debug("Subclass method check: %s", cls.__name__)  # pylint: disable=E1101
            if check_abstract and (cls.parse_field == BaseParser.parse_field or\
                cls.parse_line == BaseParser.parse_line or\
                cls.parse_string == BaseParser.parse_string):
                raise TypeError(
                    "Can't instantiate abstract class {} with unimplemented methods.".
                    format(BaseParser.__name__))

            super().__init_subclass__(**kwargs)

    def parse_field(self,
                    name,
                    field,
                    description: str = "",
                    readonly: bool = False):
        """
        Parse single field.

        It's had to be called by parse_line or parse_string.
        """
        raise NotImplementedError("Method parse_field must be implemented")

    def parse_line(self, line: str):
        """
        Parse single line.

        This abstract method is the default way for parsing streams.
        """
        raise NotImplementedError("Method parse_line must be implemented")

    def parse_string(self, string: str):
        """
        Parse a configuration as string.

        This abstract method is optional for parsing, but if you would use it,
        you should change parse_file before, or use DictField if is good for
        what you are doing.
        """
        raise NotImplementedError("Method parse_string must be implemented")

    def parse_file(self, stream: open, **kwargs):
        """Read a file; by default it read single lines."""
        fields = []
        if isinstance(stream, io.TextIOWrapper) and stream.readable():
            for line in stream:
                fields.append(self.parse_line(line, **kwargs))
            fields = RootField(
                "root", typeconf="ini", data=fields, name=stream.name)
        return fields


if sys.version_info.minor >= 6:
    _subclass_dict = dict(check_abstract=False)
else:
    # the subclass class argument is useless under 3.6
    _subclass_dict = {}


class DictParser(BaseParser, **_subclass_dict):  # pylint: disable=W0223
    """
    A partial implementation of BaseParser for dict-like configuration
    languages.

    It implements parsing of fields and a redefinition of parse_file to
    using parse_string instead of parse_line.
    This parser is good for languages that can be represented in a dict,
    such as json, yaml and ini-like files.

    .. warning::

        This implementation process only fields as dicts, array-like objects and primitive types.
        Nor comments, neither structured types are supported.
    """

    def parse_field(self, name, data, description: str = ""):  # pylint: disable=R0911
        """Parse fields keys and values."""
        if isinstance(data, bool):
            return BoolField(name, data=data, description=description)

        if isinstance(data, int):
            return IntField(name, data=data, description=description)

        if isinstance(data, float):
            return FloatField(name, data=data, description=description)

        if isinstance(data, str):
            return StringField(name, data=data, description=description)

        if isinstance(data, (list, tuple)):
            return ArrayField(
                name,
                data=[self.parse_field(None, val) for val in data],
                description=description)

            # return ArrayField(name, data=data, description=description)

        if isinstance(data, dict):
            return DictField(
                name,
                data=[self.parse_field(key, val) for key, val in data.items()],
                description=description)

        raise errhelper(
            NotImplementedError("Unimplemented data type {} of {}".format(
                type(data), data)), self.logger)  # pylint: disable=E1101

    def parse_file(self, stream: open, **kwargs):
        """Read all content of a file-like object, must be readable."""
        if isinstance(stream, io.TextIOWrapper) and stream.readable():
            root = self.parse_string(stream.read(), **kwargs)
            root.name = stream.name
            return root
        raise IOError("File isn't readable.")


class StringFieldParser(BaseParser, **_subclass_dict):  # pylint: disable=W0223
    """Partial implementation for string-only configuration languages."""

    def parse_field(self, name: str, data: str, description: str = ""):
        """The parse_field method."""
        return StringField(name, data=data, description=description)


# parsing related stuffs
class FileMatcher(ChildLoggerHelper):
    """
    Find properly class for parsing or writing.

    It provides a comunication layer between plugin manager and what
    manages files (often the frontend).
    """

    loggername = "langlib.parser.matcher"

    def __init__(self, pluginmgr):
        super().__init__()
        self.mgr = pluginmgr

    def get_language(self, lang: str, type_: str = "parser") -> BaseParser:
        """
        Get first occurence of lang searching in plugin lists.

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

    def match_filename(self, path: str):
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

    def try_parser(self, file: open, hint: BaseParser = None):
        """Try to parse the file, if parsing is successful, returns the
        parser and the parsed content."""
        parsers = list(self.mgr.loaded_parsers.values())
        if hint is not None and issubclass(hint, BaseParser):
            try:
                parser_inst = hint()
                parsed = parser_inst.parse_file(file)
                file.seek(0)
            except BadInput:
                self.logger.debug("Parser %s isn't valid for that file.",
                                  hint.__name__)
            else:
                return hint, parsed
            parsers.remove(hint)

        for parser in parsers:
            try:
                temp_parser = parser()
                parsed = temp_parser.parse_file(file)
                file.seek(0)
            except BadInput:
                self.logger.debug("Parser %s isn't valid for that file.",
                                  parser.__name__)
            else:
                return parser, parsed
        return None, None
