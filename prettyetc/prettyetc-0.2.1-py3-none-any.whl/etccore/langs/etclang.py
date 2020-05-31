#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
==========
Etc plugin
==========

Module for parsing \*nix like configuration files
(also called etc in the docs),
usually placed in /etc/ or ~/.config/.

This plugin supports:

- file parsing
- string parsing
- description attribute
- file description
- readonly attribute (When starts with #, so comment field)

Unsupported features:

- nested fields
- metadatas (partially)
"""

import io
import os
import re

import prettyetc.etccore.langlib.parsers as base
from prettyetc.etccore.langlib import Field, NameField, StringSeparatedField
from prettyetc.etccore.langlib.root import RootField
from prettyetc.etccore.plugins import PluginBase

__all__ = ("EtcParser", )

VALID_SEPARATORS = (r":", r"=")

REGEX_NAME_ONLY = re.compile(r"^\w+$")
REGEX_START_COMMENT = re.compile(r"^ *#\s", re.MULTILINE)
REGEX_FIRST_WORD = re.compile(r"^\w+\s")
REGEX_WORD_SEPARATED = re.compile(r"\w+\s*[{}]".format(
    "".join(VALID_SEPARATORS)))
REGEX_SUSPICIOUS_CHARACTERS = re.compile(r"^\s*[\+\-\$\(\)\[\]\{\}\.\<\>]+",
                                         re.MULTILINE)


class EtcParsingError(Exception):
    """Preserve useful data of a syntax error."""

    def __init__(self,
                 *args,
                 line: int = None,
                 column: int = None,
                 badstr: str = None):
        super(EtcParsingError, self).__init__(*args)
        self.line = line
        self.column = column
        self.badstr = badstr


class EtcLangParser(object):
    """
    An elastic parser that try to handle all syntaxes of etc files.

    :param bool preserve_inline_comment: If True, it adds inline comment to description.
        Default value is False.
    :param bool reset_on_empty: If True, yield all saved comment and data (after comment)
        and reset them. Default value is True.
    :param check_suspicious_characters: If True, check if there are characters in the first line
        that can be part of another language. Default value is True.

    .. warning::
        This class can change its structure, breaking the old one.
    """

    def __init__(self,
                 logger,
                 preserve_inline_comment=False,
                 reset_on_empty=True,
                 check_suspicious_characters=False):
        super().__init__()
        self.logger = logger
        self.preserve_inline_comment = preserve_inline_comment
        self.reset_on_empty = reset_on_empty
        self.check_suspicious_characters = check_suspicious_characters

    def _handle_field(self, line):
        """
        Process line and convert that in fields.

        :return: a tuple containing (in order), name, field separator, data
        :rtype: tuple(str, str, str)
        """
        data, name, sep = [""] * 3
        # is a field
        if REGEX_NAME_ONLY.match(line):
            # give " " as data to allow data to be yielded
            return line, "", " "
        if REGEX_FIRST_WORD.match(
                line) and not REGEX_WORD_SEPARATED.search(line):
            # try space separated field
            try:
                name, data = line.split(" ", 1)
            except ValueError:
                pass
            else:
                return name, " ", data

        # split as ini
        for separator in VALID_SEPARATORS:
            if line.find(separator) != -1:
                try:
                    name, data = line.split(separator, 1)
                except ValueError:
                    pass
                else:
                    sep = separator
                    break
        return name, sep, data

    def _handle_inline_comment(self, data, last_comment):
        """A component of read_string method."""
        data, _comment = data.split("#", 1)
        _comment = _comment.lstrip("#")
        data = data.rstrip("#")
        if self.preserve_inline_comment:
            if last_comment:
                last_comment += os.linesep + _comment
            else:
                last_comment = _comment
        return data, last_comment

    def _normalize_multiline(self, string):
        """
        Normalize multiline string.

        It does:
            strip the endline and the spaces
        """
        string = string.strip(os.linesep).strip()
        return string

    def _suspicious_checker(self, string):
        """Look for suspicious characters."""

        # looking for invalid symbols
        match = REGEX_SUSPICIOUS_CHARACTERS.search(string)
        if match:
            self.raise_parse_error(
                "Given etc string contains bad characters.",
                string=string,
                match=match)

    def _yield_all(self, name, sep, data, last_comment):
        """Yield all pending data."""
        if last_comment:
            # yield a comment
            yield (self._normalize_multiline(last_comment), )
        if data:
            # yield a field
            yield (name, sep, self._normalize_multiline(data))

        yield ()

    def raise_parse_error(self, *args, string=None, match=None):
        """
        Create and raise an EtcParsingError,
        by a given message and re Match object.

        .. versionadded:: 0.2.0
        """
        if match is None or string is None:
            raise EtcParsingError(*args)
        group = match.group()
        line_count = 1
        column_count = None
        last_line_pos = 0

        for i in range(match.start(), match.end()):
            if string[i] == '\n':
                line_count += 1
                last_line_pos = i

        match_line_count = group.count("\n")
        if match_line_count > 0:
            # in multiline error there is no way to know columns
            line_count = range(line_count, line_count + match_line_count)
        else:
            column_count = range(match.start() - last_line_pos,
                                 match.end() - last_line_pos)

        raise EtcParsingError(
            *args, line=line_count, column=column_count, badstr=group)

    def before_parse(self, string, multiline=False):
        """Called before parsing a string."""
        if multiline and self.check_suspicious_characters:
            self._suspicious_checker(string)

    def process_line(self, line, name, sep, data, last_comment):
        """
        Process line and yield its content.

        Except the line parameter,
        this method must return the given arguments
        (processed if necessary).
        """

        line = line.strip()

        if line == "#":
            # assuming is a \n
            self.logger.debug("Added %s to last_comment", os.linesep)
            last_comment += os.linesep

        elif REGEX_START_COMMENT.search(line):
            if data:
                # yield a field
                self.logger.debug("yield field %s%s%s", name, sep,
                                  self._normalize_multiline(data))
                yield (name, sep, self._normalize_multiline(data))
                data = ""
            line = line.lstrip("#")
            last_comment += os.linesep + line

        else:
            if last_comment:
                # yield a comment
                yield (self._normalize_multiline(last_comment), )
                last_comment = ""

            if data:
                # check if there is no fields
                if self._handle_field(line) == ("", "", ""):
                    # add new content to data
                    data += os.linesep + line

                else:
                    # yield the field and create a new one
                    yield (name, sep, self._normalize_multiline(data))
                    name, sep, data = self._handle_field(line)
                    if data.find("#") != -1:
                        data, last_comment = self._handle_inline_comment(
                            data, last_comment)
                        yield (self._normalize_multiline(last_comment), )
                        last_comment = ""

            if line.strip() == "" and self.reset_on_empty:
                # reset all data
                yield from self._yield_all(name, sep, data, last_comment)

                last_comment = ""
                name, sep, data = "", "", ""

            else:
                name, sep, data = self._handle_field(line)
                if data.find("#") != -1:
                    data, last_comment = self._handle_inline_comment(
                        data, last_comment)
                    yield (self._normalize_multiline(last_comment), )
                    last_comment = ""
        return name, sep, data, last_comment

    def read_string(self, string, multiline=False):  # pylint: disable=R0912
        """This method parse a given string and extract fields and comments."""
        data = ""
        name = ""
        sep = ""
        last_comment = ""

        self.before_parse(string, multiline)

        for line in string.split(os.linesep):
            name, sep, data, last_comment = yield from self.process_line(
                line, name, sep, data, last_comment)
        if data:
            self.logger.debug("yield field %s%s%s", name, sep,
                              self._normalize_multiline(data))
            yield (name, sep, self._normalize_multiline(data))


class EtcParser(base.StringFieldParser, PluginBase):
    """
    Parser for etc configurations.

    It uses a special parser to parse etc files.
    """

    SUFFIXES = (".conf", )
    LANGUAGES = ("etc", "sh")

    loggername = "etccore.langs.etc"

    def parse_field(self, name: str, data, description: str = "") -> Field:
        if data == "":
            return NameField(name, description=description)
        return StringSeparatedField(name, data=data, description=description)

    def parse_line(self, line: str):
        parser = EtcLangParser(self.logger.getChild("parser"))
        comment = ""
        fields = []
        for res in parser.read_string(line):
            # iter comment and lines
            if len(res) == 1:
                comment = res[0]
            elif len(res) == 3:
                name, sep, data = res
                field = self.parse_field(name, data, comment)
                field.separator = sep
                if name.startswith("#"):
                    field.name = name[1:]
                    field.readonly = True
                fields.append(field)
                comment = ""
        return field

    def parse_string(self, string: str) -> RootField:
        parser = EtcLangParser(
            self.logger.getChild("parser"), check_suspicious_characters=True)
        comment = ""
        fields = []
        root_comment = ""

        try:
            for res in parser.read_string(string, multiline=True):
                # iter comment and lines
                if not res:
                    if not root_comment and comment:
                        root_comment = comment
                    comment = ""
                    name, sep, data = "", "", ""
                if len(res) == 1:
                    comment = res[0]
                elif len(res) == 3:
                    name, sep, data = res
                    field = self.parse_field(name, data, comment)
                    field.separator = sep
                    if name.startswith("#"):
                        field.name = name[1:]
                        field.readonly = True
                    fields.append(field)
                    comment = ""

        except EtcParsingError as ex:
            raise base.BadInput(
                langname="etc",
                original_exc=ex,
                line=ex.line,
                column=ex.column,
                incriminated_string=ex.badstr)
        if fields:
            return RootField(
                "root", typeconf="etc", data=fields, description=root_comment)

        raise base.BadInput(
            langname="etc", reason="No valid data for etc is found.")

    def parse_file(self, stream: open) -> RootField:

        if isinstance(stream, io.TextIOWrapper) and stream.readable():
            try:
                root = self.parse_string(stream.read())
                root.name = stream.name
                return root

            except UnicodeDecodeError as ex:
                raise base.BadInput(
                    filename=stream.name,
                    is_valid=False,
                    # assuming that is a binary data, so there are no lines.
                    column=range(ex.start, ex.end),
                    reason=ex.reason,
                    langname=self.LANGUAGES[0],
                    original_exc=ex)
            except base.BadInput as ex:
                ex.filename = stream.name
                raise ex

        raise IOError("File isn't readable.")

    def clone(self, cls: type) -> base.BaseParser:
        """Create an instance of cls."""
        if issubclass(cls, EtcParser):
            return cls()
        raise TypeError("Given class named {} is not a subclass of {}".format(
            cls.__name__, EtcParser.__name__))
