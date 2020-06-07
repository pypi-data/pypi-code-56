#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
A set of NSD (Name Separator Data) language parsers and serializers.
"""

import io
import itertools
import os

from prettyetc.etccore.langlib import (
    BaseSerializer, Field, IndexableField, ReadAllParser, RootField,
    SeparatedField, SerializeFailed, StringSeparatedField)

from .common import (
    COMMENTS, COMMON, SEP_LANG, CommonEtcParser, optimize_grammars)

try:
    from lark import Transformer, Tree
except ImportError:
    Transformer = object

__all__ = ("SepParser", "SepSerializer")


class SepTranformer(Transformer):
    """Tranform Lark's rules into fields."""

    septype = None

    def inline_comment(self, items: list):
        """Convert an inline_comment rule into a string."""
        for token in items:
            if token.type == "ANY":
                return str(token) + "\n"
        raise ValueError("Missing content")

    def field(self, items: list) -> StringSeparatedField:
        """Convert a field rule into a StringSeparatedField."""
        # readonly check
        if items[0].type == "READONLY":
            readonly = True
            del items[0]
        else:
            readonly = False

        # get field attributes
        if len(items) > 4:
            name, sep, data, comment, *_ = items
            comment = str(comment)
        else:
            name, sep, data, *_ = items
            comment = ""
        comment = comment.strip(" \n")

        if name.startswith("#"):
            readonly = True
            name = name.lstrip("#")

        # create field
        field = StringSeparatedField(
            name, data=data, description=comment, readonly=readonly)
        field.sep = sep

        # get separator type
        if self.septype is None:
            self.septype = sep
        elif self.septype != sep:
            self.septype = ...

        return field

    def comment(self, items: list) -> str:
        """Convert a generic line comment into a string,"""
        if items[0].data == "line_comment":
            return items[0].children[0]
        if items[0].data == "empty_comment":
            return "\n"
        raise ValueError("Missing content")


class SepParser(CommonEtcParser, ReadAllParser):
    """An etc sublanguage parser that use a separator between name and data."""
    GRAMMAR = optimize_grammars(SEP_LANG, COMMON, COMMENTS)
    LANGUAGES = ("etc-sep", "etc-sep-colon", "etc-sep-equal")

    def parse_string(self, string: str) -> RootField:
        parsed = self.lark_parse(string)

        # tree tranform
        transformer = SepTranformer()
        transformed = transformer.transform(parsed)

        # sublanguage detecton
        if transformer.septype == "=":
            langname = "etc-sep-equal"
        elif transformer.septype == ":":
            langname = "etc-sep-colon"
        else:
            langname = "etc-sep"

        # rootfield creation
        root = RootField("root", data=[], langname=langname)

        # rootfield populating and comment collector
        _last_comment = ""
        for element in transformed.children:
            if isinstance(element, Tree):
                if element.data == "first_comment":
                    root.description += "".join(
                        x for x in element.children if isinstance(x, str))
                    root.description = root.description.rstrip("\n") + "\n"

            elif isinstance(element, str):
                _last_comment += element

            elif isinstance(element, Field):
                # add comment (if any) to the field
                if _last_comment:
                    element.description = (
                        _last_comment + element.description).strip(" \n")
                    _last_comment = ""
                root.add(element)
        return root


class SepSerializer(BaseSerializer):
    """An etc sublanguage writer that supports a separator between name and data."""
    LANGUAGES = ("etc-sep", "etc-sep-colon", "etc-sep-equal")

    def serialize_field(self, field: SeparatedField) -> str:
        if field.sep == ":" and self.settings.beautify:
            seriaized_field = "{}: {}".format(field.name, field.data)
        elif field.sep == "=" and self.settings.beautify:
            seriaized_field = "{} = {}".format(field.name, field.data)
        else:
            seriaized_field = "{}{}{}".format(field.name, field.sep, field.data)

        if field.readonly:
            seriaized_field = "#" + seriaized_field

        if field.description:
            if field.description.endswith("\n"):
                seriaized_field += "# " + field.description.strip("\n")
            else:
                descr = "\n".join(
                    "# " + line for line in field.description.splitlines())
                seriaized_field = "{}\n{}\n".format(descr, seriaized_field)

        return seriaized_field + "\n"

    def serialize_string(self, field: IndexableField,
                         stream: io.IOBase = None) -> str:

        langname = field.attributes["langname"] if isinstance(
            field, RootField) else None
        content = ""
        for child in itertools.chain((field,), field):
            res = None
            if isinstance(child, SeparatedField):
                res = self.serialize_field(child)
            elif isinstance(child, RootField) and child.description:
                res = "# " + "\n# ".join(
                    child.description.splitlines()).strip("\n") + "\n\n"
            elif not self.settings.silent_discard:
                raise SerializeFailed(
                    langname=langname,
                    reason=
                    "Non separated fields can't be serialzed in separated etc",
                )

            if res is not None:
                if stream is None:
                    content += res
                else:
                    stream.write(res)

        if stream is None:
            return content
        return None
