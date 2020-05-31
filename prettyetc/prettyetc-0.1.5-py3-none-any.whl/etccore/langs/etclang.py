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

import prettyetc.etccore.langlib as langlib
import prettyetc.etccore.langlib.parsers as base
from prettyetc.etccore.plugins import PluginBase

__all__ = ("EtcParser", )

VALID_SEPARATORS = (r":", r"=")

REGEX_NAME_ONLY = re.compile(r"^\w+$")
REGEX_START_COMMENT = re.compile(r"^ *#[ \n\r\t]", re.MULTILINE)
REGEX_FIRST_WORD = re.compile(r"^\w+\s")
REGEX_WORD_SEPARATED = re.compile(r"\w+\s*[{}]".format(
    "".join(VALID_SEPARATORS)))
REGEX_SUSPICIOUS_CHARACTERS = re.compile(r"^\s*[\+\-\$\(\)\[\]\{\}\.\<\>]+",
                                         re.MULTILINE)


class EtcLangParser(object):
    """
    An elastic parser that try to handle all syntaxes of etc files.

    :param preserve_inline_comment: If True, it adds inline comment to description.
        Default value is False.
    :type preserve_inline_comment: bool, optional
    :param reset_on_empty: If True, yield all saved comment and data (after comment)
        and reset them. Default value is True.
    :type reset_on_empty: bool, optional
    .. :param check_suspicious_characters: If True, check

    """

    def __init__(self,
                 preserve_inline_comment=False,
                 reset_on_empty=True,
                 check_suspicious_characters=False):
        super().__init__()
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

    def read_string(self, string, multiline=False):  # pylint: disable=R0912
        """This method parse a given string and extract fields and comments."""
        data = ""
        name = ""
        sep = ""
        last_comment = ""
        if multiline and self.check_suspicious_characters:
            # looking for invalid symbols
            if REGEX_SUSPICIOUS_CHARACTERS.search(string):
                raise EOFError("Given string contains bad characters.")
        for line in string.split(os.linesep):
            line = line.strip()
            if line == "#":
                # useless line
                continue
            elif REGEX_START_COMMENT.search(line):
                if data:
                    # yield a field
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
                    if last_comment:
                        # yield a comment
                        yield (self._normalize_multiline(last_comment), )
                    if data:
                        # yield a field
                        yield (name, sep, self._normalize_multiline(data))
                    last_comment = ""
                    name, sep, data = "", "", ""
                    yield ()
                else:
                    name, sep, data = self._handle_field(line)
                    if data.find("#") != -1:
                        data, last_comment = self._handle_inline_comment(
                            data, last_comment)
                        yield (self._normalize_multiline(last_comment), )
                        last_comment = ""

        if data:
            yield (name, sep, self._normalize_multiline(data))


class EtcParser(base.StringFieldParser, PluginBase):
    """
    Parser for etc configurations.

    It uses a special parser to parse etc files.
    """

    SUFFIXES = (".conf", )
    LANGUAGES = ("etc", "sh")

    def parse_field(self, name, data, description=""):
        if data == "":
            return langlib.NameField(name, description=description)
        return langlib.StringSeparatedField(
            name, data=data, description=description)

    def parse_line(self, line):
        parser = EtcLangParser()
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

    def parse_string(self, string):
        parser = EtcLangParser(check_suspicious_characters=True)
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
        except EOFError:
            raise base.BadInput("Given data has not valid etc syntax.")
        if fields:
            return langlib.RootField(
                "root", typeconf="etc", data=fields, description=root_comment)
        raise base.BadInput("No valid data for etc is found.")

    def parse_file(self, stream):
        if isinstance(stream, io.TextIOWrapper) and stream.readable():
            root = self.parse_string(stream.read())
            root.name = stream.name
            return root
        raise IOError("File isn't readable.")

    def clone(self, cls):
        """Create an instance of cls."""
        if issubclass(cls, EtcParser):
            return cls()
        raise TypeError("Given class named {} is not a subclass of {}".format(
            cls.__name__, EtcParser.__name__))
