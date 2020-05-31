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

import prettyetc.etccore.langlib as langlib
import prettyetc.etccore.langlib.parsers as base
from prettyetc.etccore.plugins import PluginBase

__all__ = ("IniParser", )


class IniParser(PluginBase, base.DictParser):
    """Ini parser that supports file and string parsing."""

    SUFFIXES = (".ini", "rc")
    LANGUAGES = ("ini", )

    def parse_field(self, name, data, description=""):
        """Override parse field, removing support to nested fields."""

        if data == "":
            return langlib.NameField(name, description=description)

        if isinstance(data, ini.SectionProxy):
            return langlib.DictField(
                name,
                data=[self.parse_field(key, val) for key, val in data.items()],
                description=description)

        if data.lower() in ("true", "yes", "on"):
            return langlib.BoolField(
                name=True, data=data, description=description)

        if data.lower() in ("false", "no", "off"):
            return langlib.BoolField(
                name=False, data=data, description=description)

        if data.isdigit():
            data = float(data)
            if data.is_integer():
                return langlib.IntField(
                    name, data=int(data), description=description)
            return langlib.FloatField(name, data=data, description=description)
        return langlib.StringField(name, data=data, description=description)

    def parse_line(self, line):
        """Json parsing by line is unsupported."""
        raise NotImplementedError("Ini parsing by line is unsupported.")

    def _print_parser(self, section):
        """The _print_parser method."""
        for key, value in section.items():
            if isinstance(value, ini.SectionProxy):
                self._print_parser(value)
            else:
                print("key: {}\tvalue: {}".format(key, value))

    def parse_string(self, string):
        """Parse a json file into fields."""
        parser = ini.ConfigParser()
        try:
            parser.read_string(string)
        except (ini.ParsingError, ini.DuplicateOptionError):
            raise base.BadInput("Not a valid ini file")
        fields = {}
        for key, val in parser.items():
            fields[key] = self.parse_field(key, val)
        del fields["DEFAULT"]
        return langlib.RootField("root", typeconf="ini", data=fields)
