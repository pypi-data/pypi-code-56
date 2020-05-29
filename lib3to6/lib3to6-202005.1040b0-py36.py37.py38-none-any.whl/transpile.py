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
import re
import ast
import sys
import typing as typ
try:
    import builtins
except ImportError:
    import __builtin__ as builtins
import astor
str = getattr(builtins, 'unicode', str)
from . import utils
from . import common
from . import fixers
from . import checkers
from . import fixer_base as fb
from . import checker_base as cb
DEFAULT_SOURCE_ENCODING_DECLARATION = '# -*- coding: {} -*-'
DEFAULT_SOURCE_ENCODING = 'utf-8'
DEFAULT_TARGET_VERSION = '2.7'
SOURCE_ENCODING_PATTERN = """
    ^
    [ \\t\\v]*
    \\#.*?coding[:=][ \\t]*
    (?P<coding>[-_.a-zA-Z0-9]+)
"""
SOURCE_ENCODING_RE = re.compile(SOURCE_ENCODING_PATTERN, re.VERBOSE)


def parse_module_header(module_source, target_version):
    shebang = False
    coding = None
    line = None
    header_lines = []
    for i, line_data in enumerate(module_source.splitlines()):
        if isinstance(line_data, bytes):
            line = line_data.decode(coding or DEFAULT_SOURCE_ENCODING)
        elif isinstance(line_data, str):
            line = line_data
        else:
            bad_type = type(module_source)
            errmsg = (
                "Invalid type: module_source must be str/bytes but was '{0}'"
                .format(bad_type))
            raise TypeError(errmsg)
        if i < 2:
            if i == 0 and line.startswith('#!') and 'python' in line:
                shebang = True
            else:
                match = SOURCE_ENCODING_RE.match(line)
                if match:
                    coding = match.group('coding').strip()
        if not line.rstrip() or line.rstrip().startswith('#'):
            header_lines.append(line)
        else:
            break
    if coding is None:
        coding = DEFAULT_SOURCE_ENCODING
        if target_version < '3.0':
            coding_decl = DEFAULT_SOURCE_ENCODING_DECLARATION.format(coding)
            if shebang:
                header_lines.insert(1, coding_decl)
            else:
                header_lines.insert(0, coding_decl)
    header = '\n'.join(header_lines) + '\n'
    return coding, header


CheckerType = typ.Type[cb.CheckerBase]
FixerType = typ.Type[fb.FixerBase]
CheckerOrFixer = typ.Union[CheckerType, FixerType]


def normalize_name(name):
    name = name.strip().lower().replace('_', '').replace('-', '')
    if name.endswith('fixer'):
        name = name[:-len('fixer')]
    if name.endswith('checker'):
        name = name[:-len('checker')]
    return name


def get_available_classes(module, clazz):
    assert isinstance(clazz, type)
    clazz_name = clazz.__name__
    assert clazz_name.endswith('Base')
    maybe_classes = {name: getattr(module, name) for name in dir(module) if
        not name.endswith(clazz_name)}
    return {normalize_name(attr_name): attr for attr_name, attr in
        maybe_classes.items() if type(attr) == type and issubclass(attr, clazz)
        }


FuzzyNames = typ.Union[str, typ.List[str]]


def get_selected_names(names, available_names):
    if isinstance(names, str):
        names_list = names.split(',')
    else:
        names_list = names
    selected_names = [normalize_name(name) for name in names_list if name.
        strip()]
    if selected_names:
        for name in selected_names:
            assert name in available_names
    else:
        selected_names = sorted(available_names)
    assert len(selected_names) > 0
    return selected_names


def iter_fuzzy_selected_checkers(names):
    available_classes = get_available_classes(checkers, cb.CheckerBase)
    selected_names = get_selected_names(names, set(available_classes))
    for name in selected_names:
        checker_type = typ.cast(CheckerType, available_classes[name])
        yield checker_type()


def iter_fuzzy_selected_fixers(names):
    available_classes = get_available_classes(fixers, fb.FixerBase)
    selected_names = get_selected_names(names, set(available_classes))
    for name in selected_names:
        fixer_type = typ.cast(FixerType, available_classes[name])
        yield fixer_type()


def find_import_decls(node):
    if not isinstance(node, (ast.Try, ast.Import, ast.ImportFrom)):
        return
    if isinstance(node, ast.Try):
        if not (len(node.body) == 1 and len(node.handlers) == 1):
            return
        except_handler = node.handlers[0]
        is_import_error_handler = isinstance(except_handler.type, ast.Name
            ) and except_handler.type.id == 'ImportError' and len(
            except_handler.body) == 1
        if not is_import_error_handler:
            return
        maybe_import = node.body[0]
        if isinstance(maybe_import, ast.Import):
            default_import = maybe_import
        else:
            return
        maybe_fallback_import = except_handler.body[0]
        if isinstance(maybe_fallback_import, ast.Import):
            fallback_import = maybe_fallback_import
        else:
            return
        if len(default_import.names) == 1 and len(fallback_import.names) == 1:
            default_import_alias = default_import.names[0]
            fallback_import_alias = fallback_import.names[0]
            yield common.ImportDecl(default_import_alias.name,
                default_import_alias.asname, fallback_import_alias.name)
    elif isinstance(node, ast.Import):
        if len(node.names) != 1 and any(alias.asname for alias in node.names):
            return
        else:
            alias = node.names[0]
            yield common.ImportDecl(alias.name, None, None)
    elif isinstance(node, ast.ImportFrom):
        if any(alias.asname for alias in node.names):
            return
        else:
            module_name = node.module
            if not module_name:
                return
            for alias in node.names:
                yield common.ImportDecl(module_name, alias.name, None)
    else:
        return


def parse_imports(tree):
    future_imports_offset = 0
    imports_end_offset = 0
    import_decls = set()
    for body_offset, node in enumerate(tree.body):
        is_docstring = body_offset == 0 and isinstance(node, ast.Expr
            ) and isinstance(node.value, ast.Str)
        if is_docstring:
            future_imports_offset = body_offset + 1
            imports_end_offset = body_offset + 1
            continue
        node_import_decls = list(find_import_decls(node))
        if not node_import_decls:
            break
        for import_decl in node_import_decls:
            if import_decl.module_name == '__future__':
                future_imports_offset = body_offset
            imports_end_offset = body_offset
            import_decls.add(import_decl)
    return future_imports_offset, imports_end_offset, import_decls


def add_required_imports(tree, required_imports):
    """Add imports required by fixers.

    Some fixers depend on modules which may not be imported in
    the source module. As an example, occurrences of 'map' might
    be replaced with 'itertools.imap', in which case,
    "import itertools" will be added in the module scope.

    A further quirk is that all reqired imports must be added
    before any other statment. This is because that statement
    could be subject to the fix which requires the import. As
    a side effect, a module may end up being imported twice, if
    the module is imported after some statement.
    """
    future_imports_offset, imports_end_offset, found_imports = parse_imports(
        tree)
    missing_imports = sorted(required_imports - found_imports)
    import_node = None
    for import_decl in missing_imports:
        if import_decl.import_name is None:
            import_node = ast.Import(names=[ast.alias(name=import_decl.
                module_name, asname=None)])
        else:
            import_node = ast.ImportFrom(module=import_decl.module_name,
                level=0, names=[ast.alias(name=import_decl.import_name,
                asname=None)])
        if import_decl.py2_module_name:
            asname = import_decl.import_name or import_decl.module_name
            fallback_import = ast.Import(names=[ast.alias(name=import_decl.
                py2_module_name, asname=asname)])
            import_node = ast.Try(body=[import_node], handlers=[ast.
                ExceptHandler(type=ast.Name(id='ImportError', ctx=ast.Load(
                )), name=None, body=[fallback_import])], orelse=[],
                finalbody=[])
        if import_decl.module_name == '__future__':
            tree.body.insert(future_imports_offset, import_node)
            future_imports_offset += 1
            imports_end_offset += 1
        else:
            tree.body.insert(imports_end_offset, import_node)
            imports_end_offset += 1


def add_module_declarations(tree, module_declarations):
    """Add global declarations required by fixers.

    Some fixers declare globals (or override builtins) the source
    module. As an example, occurrences of 'map' might be replaced
    by 'map = getattr(itertools, "map", map)'.

    These declarations are added directly after imports.
    """
    _, imports_end_offset, _ = parse_imports(tree)
    for decl_str in sorted(module_declarations):
        decl_node = utils.parse_stmt(decl_str)
        tree.body.insert(imports_end_offset + 1, decl_node)
        imports_end_offset += 1


def transpile_module(ctx, module_source):
    checker_names = ctx.cfg.checkers
    fixer_names = ctx.cfg.fixers
    module_tree = ast.parse(module_source)
    required_imports = set()
    module_declarations = set()
    ver = sys.version_info
    source_version = '{0}.{1}'.format(ver.major, ver.minor)
    target_version = ctx.cfg.target_version
    for checker in iter_fuzzy_selected_checkers(checker_names):
        if checker.version_info.is_applicable_to(source_version, target_version
            ):
            checker(ctx, module_tree)
    for fixer in iter_fuzzy_selected_fixers(fixer_names):
        if fixer.version_info.is_applicable_to(source_version, target_version):
            maybe_fixed_module = fixer(ctx, module_tree)
            if maybe_fixed_module is None:
                raise Exception('Error running fixer {0}'.format(type(fixer
                    ).__name__))
            required_imports.update(fixer.required_imports)
            module_declarations.update(fixer.module_declarations)
            module_tree = maybe_fixed_module
    if any(required_imports):
        add_required_imports(module_tree, required_imports)
    if any(module_declarations):
        add_module_declarations(module_tree, module_declarations)
    coding, header = parse_module_header(module_source, target_version)
    return header + ''.join(astor.to_source(module_tree))


def transpile_module_data(ctx, module_source_data):
    target_version = ctx.cfg.target_version
    coding, header = parse_module_header(module_source_data, target_version)
    module_source = module_source_data.decode(coding)
    fixed_module_source = transpile_module(ctx, module_source)
    return fixed_module_source.encode(coding)
