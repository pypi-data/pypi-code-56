#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import xml.etree.ElementTree as ET

import prettyetc.etccore.langlib as langlib
import prettyetc.etccore.langlib.parsers as base
from prettyetc.etccore.langlib import ArrayField, Field, NameField, StringField
from prettyetc.etccore.plugins import PluginBase

__all__ = ("XMLParser", )


class XMLParser(base.DictParser, PluginBase):
    SUFFIXES = (".xml", )
    LANGUAGES = ("xml", "XML")

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
                    field.append(self.parse_field(ref.tag, ref, **ref.attrib))

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

        return langlib.RootField("root", typeconf="xml", data=res)

    def parse_file(self, stream: open, **kwargs):
        """The parse_file method."""
        try:
            root = super().parse_file(stream, **kwargs)
            return root
        except Exception as ex:
            raise base.BadInput(
                filename=stream.name, langname="xml", original_exc=ex)
