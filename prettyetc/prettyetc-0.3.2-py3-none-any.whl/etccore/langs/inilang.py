#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
==========
Ini plugin
==========

Module for parsing ini.

Supports:
 - file parsing
 - string parsing
Unsupports:
 - description attribute
 - nested fields
 - metadatas
 - readonly attribute

"""

import configparser as ini

import prettyetc.etccore.langlib.parsers as base
from prettyetc.etccore.langlib import (BoolField, DictField, FloatField,
                                       IntField, NameField, StringField)
from prettyetc.etccore.langlib.root import RootField
from prettyetc.etccore.plugins import PluginBase

__all__ = ("IniParser", )


class IniParser(PluginBase, base.DictParser):
    """Ini parser that supports file and string parsing."""

    SUFFIXES = (".ini", )
    LANGUAGES = ("ini", "INI")

    def parse_field(self, name, data, description: str = "", readonly=False):
        """Override parse field, removing support to nested fields and add support for ini sections."""

        if data == "" or data is None:
            return NameField(name, description=description, readonly=readonly)

        if isinstance(data, ini.SectionProxy):
            return DictField(
                name,
                data={
                    key: self.parse_field(key, val)
                    for key, val in data.items()
                },
                description=description)

        if isinstance(data, bool):
            return BoolField(
                name=name,
                data=data,
                description=description,
                readonly=readonly)

        if data.lower() in ("true", "yes", "on"):
            return BoolField(
                name=name,
                data=True,
                description=description,
                readonly=readonly)

        if data.lower() in ("false", "no", "off"):
            return BoolField(
                name=name,
                data=False,
                description=description,
                readonly=readonly)

        try:
            data = int(data)
        except ValueError:
            pass
        else:
            return IntField(
                name, data=data, description=description, readonly=readonly)

        try:
            data = float(data)
        except ValueError:
            pass
        else:
            return FloatField(
                name, data=data, description=description, readonly=readonly)

        return StringField(
            name, data=data, description=description, readonly=readonly)

    def parse_line(self, line: str):
        """Json parsing by line is unsupported."""
        raise NotImplementedError("Ini parsing by line is unsupported.")

    def parse_string(self, string: str) -> RootField:
        """Parse a json file into fields."""
        parser = ini.ConfigParser()
        try:
            parser.read_string(string)
        except ini.MissingSectionHeaderError as ex:

            raise base.BadInput(
                langname=self.LANGUAGES[0],
                incriminated_string=ex.line,
                line=ex.lineno,
                reason=ex.message.splitlines()[0],
                original_exc=ex)

        except ini.ParsingError as ex:
            formatted_ex = base.BadInput(
                langname=self.LANGUAGES[0],
                original_exc=ex,
                reason=ex.message.splitlines()[0])

            if ex.errors:
                lineno, line = ex.errors[0]
                formatted_ex.line = lineno
                formatted_ex.incriminated_string = line

                raise formatted_ex

        except ini.InterpolationError as ex:
            raise base.BadInput(
                langname=self.LANGUAGES[0],
                reason="The given config is not a valid INI file",
                is_valid=False,
                original_exc=ex)

        except ini.DuplicateSectionError as ex:
            raise base.BadInput(
                langname=self.LANGUAGES[0],
                reason="The section {} is duplicated".format(ex.section),
                line=ex.lineno,
                incriminated_string=ex.source)

        fields = {}
        for key, val in parser.items():
            fields[key] = self.parse_field(key, val)
        del fields["DEFAULT"]
        return RootField("root", langname=self.LANGUAGES[0], data=fields)
