#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
===========
Json Plugin
===========

Module for parsing and serializing json.

Supported features:

- string parsing
- file parsing
- string serializing
- file serializing (inherited from BaseSerializer)
- nested fields

Unsupported features:

- metadata
- readonly attribute
- description attribute

.. note::
    Field description should be contained in comments but json doesn't support it.
"""

import io
import json

from prettyetc.etccore.langlib import (
    ArrayField, BadInput, BaseSerializer, DictField, Field, IndexableField,
    ReadAllParser, RootField, SerializeFailed)

try:
    # 3.5+ class
    JSONDecodeError = json.JSONDecodeError
except AttributeError:
    JSONDecodeError = ValueError

__all__ = ("JsonParser", "JsonSerializer")

_LANGUAGES = ("json",)


class JsonParser(ReadAllParser):
    """Json parser that supports file and string parsing."""

    SUFFIXES = (".json",)
    LANGUAGES = _LANGUAGES

    def parse_field(self,
                    name,
                    data,
                    description: str = "",
                    readonly=False,
                    **attributes) -> Field:
        if isinstance(data, dict):
            root_type = DictField
        elif isinstance(data, list):
            root_type = ArrayField
        field = IndexableField.from_primitives(
            data,
            description=description,
            readonly=readonly,
            root_type=root_type,
            **attributes)
        field.name = name
        return field

    def parse_line(self, line: str):
        """Json parsing by line is unsupported."""
        raise NotImplementedError("Json parsing by line is unsupported.")

    def parse_string(self, string: str, **_) -> RootField:
        """Parse a json file into fields."""
        try:
            data = json.loads(string)
        except (JSONDecodeError, UnicodeDecodeError) as ex:
            raise BadInput(langname=self.LANGUAGES[0], original_exc=ex)
        fields = self.parse_field("root", data)
        return RootField("root", langname=self.LANGUAGES[0], data=fields.data)


class JsonSerializer(BaseSerializer):
    """Json serializer that supports file (inherited from BaseSerializer) and string dumping."""

    LANGUAGES = _LANGUAGES
    STANDARD_EXTENSION = ".json"

    def serialize_field(self, field: Field) -> str:
        raise NotImplementedError("Json dumping by field is unsupported.")

    def serialize_string(self,
                         field: IndexableField,
                         stream: io.IOBase = None,
                         **_) -> str:
        if isinstance(field, IndexableField):
            field = JsonSerializer.normalize_field(field)
            primitives = field.to_primitives(use_name=True)
            indent = self.settings.indent if self.settings.beautify else None
            if stream is None:
                return json.dumps(primitives, indent=indent)
            if self.settings.beautify:
                json.dump(primitives, stream, indent=indent)
            else:
                json.dump(primitives, stream)
            return None

        raise SerializeFailed(
            langname=self.LANGUAGES[0],
            reason="IndexableField fields must be used as root field.")
