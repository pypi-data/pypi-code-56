#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
==========
Xml plugin
==========

Module for parsing xml.

Supported features:

- string parsing
- file parsing

Unsupported features:

- string serializing
- file serializing (inherited from BaseSerializer)
- metadata
- readonly attribute
- description attribute
- nested fields
"""

import xml.etree.ElementTree as ET

from prettyetc.etccore.langlib import (
    ArrayField, BadInput, BaseSerializer, Field, IndexableField, NameField,
    ReadAllParser, RootField, SerializeFailed, StringField)

__all__ = ("XMLParser", "XMLSerializer")

_LANGUAGES = ("xml", "xhtml")


class XMLParser(ReadAllParser):
    SUFFIXES = (".xml", ".xhtml")
    LANGUAGES = _LANGUAGES

    def parse_line(self, line: str):
        raise NotImplementedError("XML parsing by line is unsupported.")

    def parse_field(self,
                    name,
                    data,
                    description: str = "",
                    readonly: bool = False,
                    **attributes) -> Field:

        if data is None:
            return NameField(
                name, description=description, attributes=attributes)

        if isinstance(data, str):
            return StringField(
                name,
                data=data.strip(),
                description=description,
                attributes=attributes)

        if isinstance(data, ET.Element):
            try:
                field = ArrayField(
                    name,
                    data=[],
                    description=description,
                    attributes=attributes)

                if data.text is not None and data.text.strip():
                    field.append(self.parse_field(
                        "",
                        data.text,
                    ))
                for ref in data:
                    parsed = self.parse_field(ref.tag, ref)
                    parsed.attributes = ref.attrib
                    field.append(parsed)

                    if ref.tail is not None and ref.tail.strip():
                        field.append(self.parse_field(
                            "",
                            ref.tail,
                        ))

                return field
            except TypeError:
                return self.parse_field(data.tag, data)

        raise TypeError("Unsupported {} type".format(type(data).__name__))

    def parse_string(self, string: str):
        """Parse a xml file into fields."""
        res = []
        try:
            root = ET.fromstring(string)
            res.append(self.parse_field(root.tag, root))
        except Exception as ex:
            raise ex

        return RootField("root", langname=self.LANGUAGES[0], data=res)

    def parse_file(self, stream: open, **kwargs):
        try:
            root = super().parse_file(stream, **kwargs)
            return root
        except Exception as ex:
            raise BadInput(
                filename=stream.name, langname="xml", original_exc=ex)


class XMLSerializer(BaseSerializer):
    STANDARD_EXTENSION = ".xml"
    LANGUAGES = _LANGUAGES

    def serialize_field(self, field: Field):
        element = ET.Element("")

        if isinstance(field, RootField):
            element = ET.Element('root')
            index = 0

            for x in field:
                child = self.serialize_field(x)
                element.insert(index, child)
                index += 1

        elif isinstance(field, IndexableField):
            # Root Element
            element = ET.Element(field.name, attrib=field.attributes)

            for elem in field:
                if isinstance(elem, IndexableField):
                    element.append(self.serialize_field(elem))
                else:
                    element.text = elem.data

        elif isinstance(field, NameField):
            element = ET.Element(field.name, attrib=field.attributes)

        else:
            element = ET.Element(field.name, attrib=field.attributes)
            element.text = str(field.data)

        return element

    def serialize_string(self, field, **_):
        if isinstance(field, RootField) and field:
            # get first element of the root field
            field = list(iter(field))[0]

        return ET.tostring(
            self.serialize_field(field), encoding='utf8',
            method='xml').decode()
