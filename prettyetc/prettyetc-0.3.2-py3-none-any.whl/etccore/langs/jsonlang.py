#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
===========
Json Plugin
===========

Module for parsing json.

This plugin supports:

- file parsing
- string parsing
- nested fields

Unsupported features:

- metadatas
- readonly attribute
- description attribute

.. note::
    Field description should be contained in comments but json doesn't support it.
"""

import json

from prettyetc.etccore.langlib.root import RootField
import prettyetc.etccore.langlib.parsers as base
from prettyetc.etccore.plugins import PluginBase

try:
    # 3.5+ attribute
    JSONDecodeError = json.JSONDecodeError
except AttributeError:
    JSONDecodeError = ValueError

__all__ = ("JsonParser", )


class JsonParser(base.DictParser, PluginBase):
    """Json parser that supports file and string parsing."""

    SUFFIXES = (".json", )
    LANGUAGES = ("json", "JSON")

    def parse_line(self, line: str):
        """Json parsing by line is unsupported."""
        raise NotImplementedError("Json parsing by line is unsupported.")

    def parse_string(self, string: str, **_) -> RootField:
        """Parse a json file into fields."""
        try:
            data = json.loads(string)
        except (JSONDecodeError, UnicodeDecodeError) as ex:
            raise base.BadInput(langname="json", original_exc=ex)
        if isinstance(data, list):
            fields = []
            for val in data:
                fields.append(self.parse_field("", val))
        elif isinstance(data, dict):
            fields = {}
            for key, val in data.items():
                fields[key] = self.parse_field(key, val)
        else:
            raise NotImplementedError(
                "Unimplemented root data type {} of {}".format(
                    type(data), data))
        return RootField("root", langname="json", data=fields)
