# -*- coding: utf-8 -*-
# This file is part of the lib3to6 project
# https://gitlab.com/mbarkhau/lib3to6
#
# Copyright (c) 2019 Manuel Barkhau (mbarkhau@gmail.com) - MIT License
# SPDX-License-Identifier: MIT

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
import ast
import typing as typ
import astor
from . import common
from . import transpile
NodeOrNodelist = typ.Union[ast.AST, typ.List[typ.Any]]


def dump_ast(node, annotate_fields=True, include_attributes=False, indent='  '
    ):
    """Return a formatted dump of the tree in *node*.

    This is mainly useful for debugging purposes.  The returned
    string will show the names and the values for fields.  This
    makes the code impossible to evaluate, so if evaluation is
    wanted *annotate_fields* must be set to False.  Attributes
    such as line numbers and column offsets are not dumped by
    default.  If this is wanted, *include_attributes* can be set
    to True.
    """

    def _format(node, level=1):
        if isinstance(node, ast.AST):
            fields = [(a, _format(b, level + 1)) for a, b in ast.
                iter_fields(node)]
            if include_attributes and node._attributes:
                fields.extend([(a, _format(getattr(node, a), level + 1)) for
                    a in node._attributes])
            if annotate_fields:
                field_parts = [('%s=%s' % field) for field in fields]
            else:
                field_parts = [b for a, b in fields]
            node_name = node.__class__.__name__
            is_short_node = len(field_parts) <= 1 or isinstance(node, (ast.
                Name, ast.Num, ast.Str, ast.Bytes, ast.alias))
            if is_short_node:
                return node_name + '(' + ', '.join(field_parts) + ')'
            lines = [node_name + '(']
            for part in field_parts:
                lines.append(indent * level + part + ',')
            lines.append(indent * (level - 1) + ')')
            return '\n'.join(lines)
        elif isinstance(node, list):
            subnodes = typ.cast(typ.List[typ.Any], node)
            if len(subnodes) == 0:
                return '[]'
            if len(subnodes) == 1:
                return '[' + _format(subnodes[0], level) + ']'
            lines = [(indent * level + _format(subnode, level + 1) + ',') for
                subnode in subnodes]
            return '[\n' + '\n'.join(lines) + '\n' + indent * (level - 1) + ']'
        return repr(node)
    if isinstance(node, (ast.AST, list)):
        return _format(node)
    else:
        raise TypeError('expected AST, got %r' % node.__class__.__name__)


def clean_whitespace(fixture_str):
    if fixture_str.strip().count('\n') == 0:
        return fixture_str.strip()
    fixture_lines = [line for line in fixture_str.splitlines() if line.strip()]
    line_indents = [(len(line) - len(line.lstrip())) for line in fixture_lines]
    if not any(line_indents) or min(line_indents) == 0:
        return fixture_str
    indent = min(line_indents)
    dedented_lines = [line[indent:] for line in fixture_lines]
    return '\n'.join(dedented_lines).strip() + '\n'


def parse_stmt(code):
    module = ast.parse(code)
    assert len(module.body) == 1
    return module.body[0]


def parsedump_ast(code, mode='exec', **kwargs):
    """Parse some code from a string and pretty-print it."""
    node = ast.parse(clean_whitespace(code), mode=mode)
    return dump_ast(node, **kwargs)


def parsedump_source(code, mode='exec'):
    node = ast.parse(clean_whitespace(code), mode=mode)
    return astor.to_source(node)


def transpile_and_dump(ctx, module_str):
    module_str = clean_whitespace(module_str)
    coding, header = transpile.parse_module_header(module_str, ctx.cfg.
        target_version)
    result_str = transpile.transpile_module(ctx, module_str)
    return coding, header, result_str


def has_base_class(cls_node, module_name=None, base_class_name=None):
    if not (module_name or base_class_name):
        return False
    for base in cls_node.bases:
        if isinstance(base, ast.Attribute):
            val = base.value
            if isinstance(val, ast.Name
                ) and val.id == module_name and base.attr == base_class_name:
                return True
        if isinstance(base, ast.Name) and base.id == base_class_name:
            return True
    return False
