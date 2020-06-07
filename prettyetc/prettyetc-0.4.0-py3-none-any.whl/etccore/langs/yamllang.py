#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
===========
Yaml Plugin
===========

Module for parsing and serializing yaml.

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

from ruamel.yaml import YAML
from ruamel.yaml.composer import ComposerError
from ruamel.yaml.constructor import DuplicateKeyError
from ruamel.yaml.scanner import ScannerError

from prettyetc.etccore.langlib import (
    ArrayField, BadInput, BaseSerializer, DictField, Field, IndexableField,
    ReadAllParser, RootField, SerializeFailed)

__all__ = ("YamlParser", "YamlSerializer")

_LANGUAGES = ("yaml",)


class YamlParser(ReadAllParser):
    """Yaml parser that supports both file and string parsing."""

    SUFFIXES = (".yaml",)
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
        else:
            raise BadInput(
                langname=self.LANGUAGES[0],
                reason="Yaml only supports complex data")
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

    def parse_string(self, string):
        """Parse a yaml file into fields."""
        # init YAML
        yaml = YAML()

        # set default indent to 4
        yaml.indent(mapping=4)  # pylint: disable = E1102

        # find if using default_flow_style
        if string.find(": {") != -1:
            yaml.default_flow_style = True
        else:
            yaml.default_flow_style = False

        # find if using explicit_start and/or explicit_end
        yaml.explicit_start = string.startswith("---")
        yaml.explicit_end = string.endswith("...")

        # parse raw_input
        try:
            data = yaml.load(string)
        except ScannerError as ex:
            raise BadInput(
                langname=self.LANGUAGES[0],
                reason=ex.problem,
                incriminated_string="\n".join(
                    ex.problem_mark.get_snippet().splitlines()[:-1]),
                line=ex.problem_mark.line,
                column=ex.problem_mark.column,
                original_exc=ex,
            )

        except (ComposerError, DuplicateKeyError) as ex:
            if ex.context is not None:
                problem = ex.context + ", " + ex.problem
            else:
                problem = ex.problem
            raise BadInput(
                langname=self.LANGUAGES[0],
                reason=problem,
                incriminated_string="\n".join(
                    ex.problem_mark.get_snippet().splitlines()[:-1]),
                line=ex.problem_mark.line,
                column=ex.problem_mark.column,
                original_exc=ex,
            )

        fields = self.parse_field("root", data)
        rootField = YamlRootField(
            yaml, "root", langname=self.LANGUAGES[0], data=fields.data)
        return rootField


class YamlSerializer(BaseSerializer):
    """Yaml serializer that supports file (inherited from BaseSerializer) and string dumping."""

    LANGUAGES = _LANGUAGES
    STANDARD_EXTENSION = ".yaml"

    def serialize_field(self, field: Field) -> str:
        raise NotImplementedError("Yaml dumping by field is unsupported.")

    def serialize_string(self,
                         field: IndexableField,
                         stream: io.IOBase = None,
                         **_) -> str:
        if isinstance(field, IndexableField):
            primitives = field.to_primitives(use_name=True)
            indent = self.settings.indent if self.settings.beautify else None
            if stream is None:
                stream = io.StringIO()
            # check if yaml settings are present in the field
            if isinstance(field, YamlRootField):
                field.yaml.dump(primitives, stream=stream)
            else:
                yaml = YAML()
                # respect config.beautify only if there are no yaml settings
                # present in the field
                if self.settings.beautify:
                    yaml.indent = indent
                    yaml.explicit_start = True
                    yaml.explicit_end = True
                    yaml.default_flow_style = False
                yaml.dump(primitives, stream=stream)
            if isinstance(stream, io.StringIO):
                return stream.read()
            return None

        raise SerializeFailed(
            langname=self.LANGUAGES[0],
            reason="IndexableField fields must be used as root field.")


class YamlRootField(RootField):
    """
    this is a RootField with the added attribute "yaml" which contains the
    original file options (used when serializing).
    """

    __slots__ = ("yaml",)

    def __init__(self, yaml, *args, **kwargs):
        super(YamlRootField, self).__init__(*args, **kwargs)
        self.yaml = yaml
