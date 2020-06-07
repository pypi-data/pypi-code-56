#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
==========
Ini plugin
==========

Module for parsing and serializing ini.

Supported features:

- string parsing
- file parsing
- string serializing
- file serializing (inherited from BaseSerializer)

Unsupported features:

- metadata
- readonly attribute
- description attribute
- nested fields
"""

import configparser as ini
import io

from prettyetc.etccore.langlib import (
    BadInput, BaseSerializer, BoolField, DictField, Field, FloatField,
    IndexableField, IntField, NameField, ReadAllParser, RootField,
    SerializeFailed, StringField)
from prettyetc.etccore.plugins import PluginBase

__all__ = ("IniParser", "IniSerializer")
_LANGUAGES = ("ini",)


class IniParser(PluginBase, ReadAllParser):
    """Ini parser that supports file and string parsing."""

    SUFFIXES = (".ini",)
    LANGUAGES = _LANGUAGES

    def parse_field(self, name, data, description: str = "",
                    readonly=False) -> Field:

        if data == "" or data is None:
            return NameField(name, description=description, readonly=readonly)

        if isinstance(data, ini.SectionProxy):
            return DictField(
                name,
                data={
                    key: self.parse_field(key, val)
                    for key, val in data.items()
                },
                description=description,
                readonly=readonly)

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
        """Ini parsing by line is unsupported."""
        raise NotImplementedError("Ini parsing by line is unsupported.")

    def parse_string(self, string: str) -> RootField:
        parser = ini.ConfigParser()
        try:
            parser.read_string(string)
        except ini.MissingSectionHeaderError as ex:

            raise BadInput(
                langname=self.LANGUAGES[0],
                incriminated_string=ex.line,
                line=ex.lineno,
                reason=ex.message.splitlines()[0],
                original_exc=ex)

        except ini.ParsingError as ex:
            formatted_ex = BadInput(
                langname=self.LANGUAGES[0],
                original_exc=ex,
                reason=ex.message.splitlines()[0])

            if ex.errors:
                lineno, line = ex.errors[0]
                formatted_ex.line = lineno
                formatted_ex.incriminated_string = line

                raise formatted_ex

        except ini.InterpolationError as ex:
            raise BadInput(
                langname=self.LANGUAGES[0],
                reason="The given config is not a valid INI file",
                is_valid=False,
                original_exc=ex)

        except ini.DuplicateSectionError as ex:
            raise BadInput(
                langname=self.LANGUAGES[0],
                reason="The section {} is duplicated".format(ex.section),
                line=ex.lineno,
                incriminated_string=ex.source)

        fields = {}
        for key, val in parser.items():
            fields[key] = self.parse_field(key, val)
        del fields["DEFAULT"]
        return RootField("root", langname=self.LANGUAGES[0], data=fields)


class IniSerializer(BaseSerializer):
    """Ini serializer that supports file (inherited from BaseSerializer) and string dumping."""

    LANGUAGES = _LANGUAGES
    STANDARD_EXTENSION = ".ini"

    def serialize_field(self, field: Field) -> str:
        if isinstance(field, NameField):
            return None
        if isinstance(field, BoolField):
            return "yes" if field else "no"
        if isinstance(field, (IntField, FloatField, StringField)):
            return str(field.data)
        if not self.settings.silent_discard:
            raise SerializeFailed(
                langname=self.LANGUAGES[0],
                reason="Composite fields can't be an INI property")
        return ...

    def serialize_string(  # pylint: disable=R1710
            self,
            field: IndexableField,
            stream: io.IOBase = None,
            **_) -> str:
        if stream is None:
            _stream = io.StringIO()

        writer = ini.ConfigParser()
        if isinstance(field, IndexableField):
            for key, child in field.iteritems():
                # only indexable fields are allowed
                if isinstance(child, IndexableField):
                    # create a new section
                    key = str(key)
                    writer[key] = {}

                    for name, val in child.iteritems():
                        data = self.serialize_field(val)
                        if data != ...:
                            writer[key][str(name)] = data

                elif not self.settings.silent_discard:
                    raise SerializeFailed(
                        langname=self.LANGUAGES[0],
                        reason=
                        "INI properties can't be serialized without a section")

        else:
            raise SerializeFailed(
                langname=self.LANGUAGES[0],
                reason="INI properties can't be serialized without a section")

        if stream is None:
            writer.write(_stream)
            return _stream.getvalue()
        writer.write(stream)
