#!/usr/bin/env python3
# -*- coding: utf-8 -*-

##########################################################
#
# THIS MODULE IS A USELESS TRY TO IMPLEMENT A YAML PARSER
#
##########################################################
"""
Yaml parser module.

Supports:
    - file parsing
    - string parsing
    - nested fields
Unsupported:
- readonly attribute
TODO:
- description attribute
.. note::
ruamel.yaml comments isn't so stable and its implemenation is hard.

"""

import prettyetc.etccore.langlib.parsers as base

__all__ = ()


class YamlParser(base.BaseParser):
    """Yaml parser that supports both file and string parsing."""

    def parse_field(self, name, data):  # pylint: disable=R0911
        """Parse json keys."""
        if isinstance(data, bool):
            return base.BoolField(name, data=data)

        if isinstance(data, int):
            return base.IntField(name, data=data)

        if isinstance(data, float):
            return base.FloatField(name, data=data)

        if isinstance(data, str):
            return base.StringField(name, data=data)

        if isinstance(data, list, tuple):
            if any(isinstance(val, list, tuple, dict) for val in data):
                return base.ArrayField(
                    name, data=[self.parse_field("", val) for val in data])

            return base.ArrayField(name, data=data)

        if isinstance(data, dict):
            return base.ArrayField(
                name,
                data=[self.parse_field(key, val) for key, val in data.items()])

        raise TypeError("Unimplemented data type {} of {}".format(
            type(data), data))

    def parse_line(self, line):
        """Yaml parsing by line is unsupported."""
        raise NotImplementedError("Yaml parsing by line is unsupported.")

    def parse_string(self, string):
        """Parse a json file into fields."""
        # data = yaml.load(string)
        data = []
        if isinstance(data, list):
            fields = []
            for val in data:
                fields.append(self.parse_field("", val))
        elif isinstance(data, dict):
            fields = {}
            for key, val in data.values():
                fields[key] = self.parse_field(key, val)
        else:
            raise NotImplementedError()
        return fields

    def parse_file(self, steam):
        """Read a file; by default it read single lines."""
        if steam.readable():
            return self.parse_string(steam.read())
        raise IOError("File isn't readable.")
