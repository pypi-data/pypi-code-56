#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
A set of space separated language parsers and serializers
"""

import io

from prettyetc.etccore.langlib import (
    ArrayField, BadInput, BaseSerializer, Field, IndexableField, ReadAllParser,
    RootField, SerializeFailed, StringField)

from .common import SPACE_LANG, CommonEtcParser, optimize_grammars

try:
    from lark import Transformer
    from lark.exceptions import VisitError
except ImportError:
    Transformer = object

__all__ = ("SpaceParser", "WordListSpaceSerializer", "WordPairSpaceSerializer",
           "SpaceSepSerializer")


class SpaceTranformer(Transformer):
    """
    Tranform Lark's rules into fields.

    Also keep the field lines lenght to obtain language name
    """
    max_len = -1
    min_len = -1

    def field(self, items: list):
        """Convert a field rule into the properly field."""
        if items[0].type == "COMMENT_CHAR":
            return " ".join(items[1:]) + "\n"

        _old_items = items.copy()
        items.clear()
        readonly = False
        for item in _old_items:
            if item.type == "WORD":
                items.append(item)
            elif item.type == "READONLY":
                readonly = True

        item_len = len(items)
        if item_len < self.min_len or self.min_len == -1:
            self.min_len = item_len
        if item_len > self.max_len:
            self.max_len = item_len

        retfield = ArrayField(
            str(items[0]),
            data=[],
            readonly=readonly,
        )
        for item in items[1:]:
            data = str(item)
            if data in ("=", ":"):
                raise BadInput(
                    langname="etc-sep-space",
                    reason=
                    "This file contains separators that should be handled by etc-sep"
                )

            retfield.add(StringField(
                None,
                data=data,
                readonly=readonly,
            ))

        if item_len == 1 and set('=:').intersection(items[0]):
            raise BadInput(
                langname="etc-sep-space",
                reason=
                "This file contains separators that should be handled by etc-sep"
            )

        return retfield


class SpaceParser(CommonEtcParser, ReadAllParser):
    """An etc sublanguage parser that use spaces (or tabs) between name and data."""
    GRAMMAR = optimize_grammars(SPACE_LANG)
    LANGUAGES = ("etc-wordlist", "etc-wordpair", "etc-sep-space")

    def parse_string(self, string: str) -> RootField:
        parsed = self.lark_parse(string)

        # tree tranform
        transformer = SpaceTranformer()
        try:
            transformed = transformer.transform(parsed)
        except VisitError as ex:
            raise ex.orig_exc

        len_pair = (transformer.min_len, transformer.max_len)
        if transformer.max_len > 2 and transformer.min_len > 1:
            langname = "etc-sep-space"
        elif len_pair == (1, 1):
            langname = "etc-wordlist"
        elif len_pair == (2, 2):
            langname = "etc-wordpair"
        else:
            raise BadInput(
                langname="etc-sep-space",
                reason="Cannot mix single words with word pairs.")

        # rootfield creation
        root = RootField("root", data=[], langname=langname)

        # rootfield populating and comment collector
        _last_comment = ""
        for element in transformed.children:
            if isinstance(element, str):
                _last_comment += element

            elif isinstance(element, Field):
                if langname == "etc-wordlist":
                    element = StringField(
                        None, data=element.name, readonly=element.readonly)
                elif langname == "etc-wordpair":
                    element = StringField(
                        element.name,
                        data=element.data[0].data,
                        readonly=element.readonly)

                # add comment (if any) to the field
                if _last_comment:
                    element.description = _last_comment.strip(" \n")
                    _last_comment = ""
                root.add(element)
        return root


class SpaceSerializer(BaseSerializer):
    """An etc sublanguage writer that supports a separator between name and data."""

    # LANGUAGES = ("etc-wordlist", "etc-wordpair", "etc-sep-space")
    LANGUAGES = ()

    def _complex_error(self, language: str):
        if not self.settings.silent_discard:
            raise SerializeFailed(
                langname=language,
                reason="Complex fields can't be serialzed in space separated etc"
            )

    def serialize_field(self, field: Field) -> str:
        language = self.LANGUAGES[0]

        if language == "etc-wordlist":
            # word
            if isinstance(field, IndexableField):
                return self._complex_error(language)

            seriaized_field = str(field)

        elif language == "etc-wordpair":
            # name data
            if isinstance(field, IndexableField):
                return self._complex_error(language)
            seriaized_field = "{} {}".format(field.name, field.data)

        else:
            # name some data
            data_serialized = ""
            for child in field:
                if isinstance(field, IndexableField):
                    self._complex_error(language)
                else:
                    data_serialized += "{} ".format(child)

            data_serialized = data_serialized.rstrip(" ")
            seriaized_field = "{} {}".format(field.name, data_serialized)

        if field.readonly:
            seriaized_field = "#" + seriaized_field

        if field.description:
            # add description
            descr = "\n".join(
                "# " + line for line in field.description.splitlines())
            seriaized_field = "{}\n{}\n".format(descr, seriaized_field)

        return seriaized_field + "\n"

    def serialize_string(self, field: IndexableField,
                         stream: io.IOBase = None) -> str:
        content = ""
        for child in field:
            res = self.serialize_field(child)

            if res is not None:
                if stream is None:
                    content += res
                else:
                    stream.write(res)

        if stream is None:
            return content
        return None


class WordListSpaceSerializer(SpaceSerializer):
    """An etc-wordlist language serializer."""

    LANGUAGES = ("etc-wordlist",)


class WordPairSpaceSerializer(SpaceSerializer):
    """An etc-wordpair language serializer."""

    LANGUAGES = ("etc-wordpair",)


class SpaceSepSerializer(SpaceSerializer):
    """An etc-sep-space language serializer."""

    LANGUAGES = ("etc-sep-space",)
