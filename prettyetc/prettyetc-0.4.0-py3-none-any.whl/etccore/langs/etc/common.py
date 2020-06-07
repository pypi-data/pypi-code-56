#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Root of the etc language collection."""
from collections import OrderedDict

from prettyetc.etccore.langlib import (
    BadInput, BaseParser, Field, NameField, StringField, StringSeparatedField)

try:
    from lark import Tree, Lark, UnexpectedCharacters
except ImportError:
    Tree = None

__all__ = ("COMMON", "COMMENTS", "SEP_LANG", "CommonEtcParser",
           "optimize_grammars", "SPACE_LANG")
# A list of grammar chunks to be assembled in etc sublanguages

COMMON = r"""
ANY: /.+/
READONLY: "#"

NEWLINE: (CR? LF)

%import common.CR
%import common.LF
"""
"""A collection of generic rules."""

COMMENTS = r"""
inline_comment: "#"+ WS_INLINE ANY WS_INLINE? "#"*

line_comment: inline_comment NEWLINE
empty_comment: "#"+ WS_INLINE? NEWLINE

comment: (line_comment | empty_comment)
first_comment: NEWLINE* comment+ NEWLINE+

%import common.WS
%import common.WS_INLINE

"""
"""
A rule to get line comments.

Depends on COMMON
"""

SEP_LANG = r"""

start: first_comment? (comment | field | NEWLINE)+

NAME: /[\.\w#]+/
DATA: /[^#\n]+/
SEP: WS_INLINE? /[=:]/ WS_INLINE?

field: NAME SEP DATA [inline_comment] NEWLINE

%import common.WS_INLINE
// %ignore NEWLINE
"""
"""
An NSD (Name Sep Data) language.

Depends on COMMENTS and COMMON
"""

SPACE_LANG = r"""
start: field+
WORD: /[^ \t\f\r\n]+/

READONLY: "#"
COMMENT_CHAR: "# "

field: (COMMENT_CHAR | READONLY)? (WORD WS_INLINE?)+ NEWLINE

%import common.WS_INLINE
%ignore WS_INLINE
%import common.NEWLINE
// %ignore NEWLINE
"""


def optimize_grammars(*grammars: str) -> str:
    """Optimize the given gramars and reducing possibly errors
    created by joining different grammar chunks."""
    grammar = ""
    for grm in grammars:
        grammar += grm + "\n"

    retgrm = ""
    for line in list(OrderedDict.fromkeys(grammar.splitlines())):
        if line:
            retgrm += line + "\n"

    return retgrm


class CommonEtcParser(BaseParser):  # pylint: disable=W0223
    """A base for the etc parsers."""

    GRAMMAR = None

    def parse_field(self,
                    name,
                    data,
                    description: str = "",
                    readonly: bool = False,
                    sep: str = None,
                    **attributes):

        if data is None:
            return NameField(
                name, description=description, readonly=readonly, **attributes)
        if sep is None:
            return StringField(
                name,
                data=data,
                description=description,
                readonly=readonly,
                **attributes)

        field = StringSeparatedField(
            name,
            data=data,
            description=description,
            readonly=readonly,
            **attributes)
        field.sep = sep
        return field

    def parse_line(self, line: str) -> Field:
        root = self.parse_string(line)
        if root:
            return root[0]
        raise BadInput()

    def lark_parse(self, string: str) -> Tree:
        """
        Parse a string using lark-parser grammar.

        The grammar must be defined in the class.
        """
        if not string.strip(" \n"):
            return Tree("", [])

        if not string.endswith("\n"):
            string += "\n"
        if getattr(self, "GRAMMAR", None) is None:
            raise NotImplementedError("Missing etc grammar")
        try:
            # TODO: use larl parser
            parsed = Lark(self.GRAMMAR).parse(string)

        except UnexpectedCharacters as ex:
            # raise an equivalent badinput
            raise BadInput(
                langname=self.LANGUAGES[0],
                reason=ex.args
                if isinstance(ex.args, str) else " ".join(ex.args),
                line=ex.line,
                column=ex.column,
                original_exc=ex,
                is_valid=ex.line > 0)

        return parsed
