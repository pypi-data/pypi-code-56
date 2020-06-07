#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
==========
Etc plugin
==========

Module for parsing \*nix like configuration files
(also called etc in the docs),
usually placed in /etc/ or ~/.config/.

Supported features:

- string parsing
- file parsing
- description attribute
- metadata (partially)
- readonly attribute (When \# is found, so comment field)
- file description (comment at the beginning of the file)

Unsupported features:

- string serializing
- file serializing (inherited from BaseSerializer)
- nested fields
"""

import io
import os
import re

from prettyetc.etccore.langlib import (
    BadInput, BaseParser, Field, NameField, RootField, StringSeparatedField)

try:
    from lark import Lark, Tree, UnexpectedCharacters
except ImportError:
    Lark = None
    Tree = None
    __all__ = ("EtcParser",)
else:
    __all__ = ()

VALID_SEPARATORS = (r":", r"=")

REGEX_NAME_ONLY = re.compile(r"^\w+$")
REGEX_START_COMMENT = re.compile(r"^ *#\s", re.MULTILINE)
REGEX_FIRST_WORD = re.compile(r"^\w+\s")
REGEX_WORD_SEPARATED = re.compile(r"\w+\s*[{}]".format(
    "".join(VALID_SEPARATORS)))
REGEX_SUSPICIOUS_CHARACTERS = re.compile(r"^\s*[\+\-\$\(\)\[\]\{\}\.\<\>]+",
                                         re.MULTILINE)

etc_grammar = r"""
start: (comment
        | field
        | name_only)+

NAME: /^[\.\w]+/m
name_only: NAME [WS_INLINE] [inline_comment] NEWLINE
DATA: /[^#\n]+/

STRING: /.+$/m

SEP: /[=:]/ | WS_INLINE
COMMENT_CHAR: "#" WS_INLINE*

inline_comment: COMMENT_CHAR [STRING]
comment.10: inline_comment NEWLINE

field: NAME SEP DATA [inline_comment] NEWLINE

%import common.WS
%import common.WS_INLINE
%import common.SIGNED_NUMBER
%import common.WORD
%import common.NEWLINE

//%ignore WS
//%ignore WS_INLINE
"""
_LANGUAGES = ("etc", "sh")


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


class InternalEtcParser(object):
    """
    An elastic parser that tries to handle all syntaxes of etc files.

    :param bool preserve_inline_comment: If True, it adds the inline comment to the Field description.
        Default value is False.

    :param bool reset_on_empty: If True and the line after the Field is empty,
        yield all saved comment and data (after comment).

        Default value is True.

    :param bool check_suspicious_characters:
        If True, check if there are characters in the first line that can be part of another language.
        This will be moved elsewhere in the future.

        Default value is True.
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

        - strip the endline and the spaces
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
            yield (self._normalize_multiline(last_comment),)
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
                yield (self._normalize_multiline(last_comment),)
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
                        yield (self._normalize_multiline(last_comment),)
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
                    yield (self._normalize_multiline(last_comment),)
                    last_comment = ""
        return name, sep, data, last_comment

    def read_string(self, string, multiline=False):
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


class EtcParser(BaseParser):
    """
    Parser for etc configurations.

    It uses a special parser to parse etc files.
    """

    # SUFFIXES = (".conf",)
    LANGUAGES = _LANGUAGES

    loggername = "etccore.langs.etc"

    def _raise_badinput(self, element: Tree):
        """Raise a BadInput, given Tree object."""

        children = element.children
        line = None
        incriminated_string = None
        for token in children:
            if line is None:
                line = token.line
                incriminated_string = ""
            incriminated_string += token.value

        raise BadInput(
            langname=self.LANGUAGES[0],
            reason="Malformed field.",
            line=line,
            incriminated_string=incriminated_string)

    def _comment_tostring(self, element: Tree,
                          newline: str = os.linesep) -> str:
        """Convert Lark Tree object, with its children, in a string."""
        if element.data == "comment":
            children = element.children[0].children
        elif element.data == "inline_comment":
            children = element.children

        if len(children) == 1:
            comment = newline
        else:
            token = children[1]
            comment = token.value + newline

        return comment

    def _process_field(self, element: Tree, name_only: bool = False) -> Field:
        """Convert Lark Tree object, with its children, in a Field object."""
        children = element.children
        if name_only:

            if len(children) < 2:
                self._raise_badinput(element)

            elif len(children) == 2:
                name, _ = children

                field = self.parse_field(
                    name.value, data="", description=None)  # flag

            elif len(children) == 3:

                name, token, _ = children
                if token.type == "WS_INLINE":
                    comment = None  # flag
                else:
                    comment = token.value

                field = self.parse_field(
                    name.value, data=None, description=comment)

            else:
                name, _, comment, *_ = children

                field = self.parse_field(
                    name.value,
                    data=None,
                    description=self._comment_tostring(comment, newline=""))

        else:
            if len(children) < 4:
                self._raise_badinput(element)

            elif len(children) == 4:
                name, sep, data, _ = children
                field = self.parse_field(
                    name=name.value, data=data.value, description=None)  # flag
                field.sep = sep.value

            else:
                name, sep, data, comment, *_ = children
                field = self.parse_field(
                    name=name.value,
                    data=data.value,
                    description=self._comment_tostring(comment))
                field.sep = sep.value

        return field

    def parse_field(self, name: str, data, description: str = "") -> Field:
        if data == "":
            return NameField(name, description=description)
        return StringSeparatedField(name, data=data, description=description)

    def parse_line(self, line: str):
        parser = InternalEtcParser(self.logger.getChild("parser"))
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
        if Lark is None:
            return self.parse_string_embedded(string)
        return self.parse_string_lark(string)

    def parse_string_lark(self, string: str) -> RootField:
        """Parse etc syntax using Lark parser."""

        try:
            # TODO: use larl parser
            parsed = Lark(etc_grammar).parse(string)

        except UnexpectedCharacters as ex:
            raise BadInput(
                langname=self.LANGUAGES[0],
                reason=ex.args
                if isinstance(ex.args, str) else " ".join(ex.args),
                line=ex.line,
                column=ex.column,
                original_exc=ex,
                is_valid=ex.line > 0)

        _last_comment = ""
        fields = []
        for element in parsed.iter_subtrees():
            if element.data == "comment":
                _last_comment += self._comment_tostring(element)

            elif element.data == "empty_comment":
                _last_comment += "\n"

            elif element.data == "field":

                field = self._process_field(element)
                if field.description is None:
                    field.description = _last_comment.rstrip()
                    _last_comment = ""
                fields.append(field)

            elif element.data == "name_only":

                field = self._process_field(element, True)

                if field.description is None:
                    field.description = _last_comment
                    _last_comment = ""

                fields.append(field)
        if fields:
            return RootField("root", langname="etc", data=fields)

        raise BadInput(langname="etc", reason="No valid data for etc is found.")

    def parse_string_embedded(self, string: str) -> RootField:
        """Parse etc syntax using plugin embedded parser."""
        parser = InternalEtcParser(
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
            raise BadInput(
                langname="etc",
                original_exc=ex,
                line=ex.line,
                column=ex.column,
                incriminated_string=ex.badstr)
        if fields:
            return RootField(
                "root", typeconf="etc", data=fields, description=root_comment)

        raise BadInput(
            langname=self.LANGUAGES[0],
            reason="No valid data for etc is found.")

    def parse_file(self, stream: open) -> RootField:
        if isinstance(stream, io.TextIOWrapper) and stream.readable():
            try:
                root = self.parse_string(stream.read())
                root.name = stream.name
                return root

            except UnicodeDecodeError as ex:
                raise BadInput(
                    filename=stream.name,
                    is_valid=False,
                    # assuming that is a binary data, so there are no lines.
                    column=range(ex.start, ex.end),
                    reason=ex.reason,
                    langname=self.LANGUAGES[0],
                    original_exc=ex)
            except BadInput as ex:
                ex.filename = stream.name
                raise ex

        raise IOError("File isn't readable.")
