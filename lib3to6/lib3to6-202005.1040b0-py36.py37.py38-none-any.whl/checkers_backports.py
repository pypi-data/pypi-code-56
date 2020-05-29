# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
import ast
import typing as typ
try:
    import builtins
except ImportError:
    import __builtin__ as builtins
import logging
str = getattr(builtins, 'unicode', str)
from . import common
from . import checker_base as cb
log = logging.getLogger(__name__)
ModuleVersionInfo = typ.NamedTuple('ModuleVersionInfo', [('available_since',
    str), ('backport_module', typ.Optional[str]), ('backport_package', typ.
    Optional[str])])
MAYBE_UNUSABLE_MODULES = {'asyncio': ModuleVersionInfo('3.4', None, None),
    'zipapp': ModuleVersionInfo('3.5', None, None), 'csv':
    ModuleVersionInfo('3.0', 'backports.csv', 'backports.csv'), 'selectors':
    ModuleVersionInfo('3.4', 'selectors2', 'selectors2'), 'pathlib':
    ModuleVersionInfo('3.4', 'pathlib2', 'pathlib2'), 'importlib.resources':
    ModuleVersionInfo('3.7', 'importlib_resources', 'importlib_resources'),
    'inspect': ModuleVersionInfo('3.6', 'inspect2', 'inspect2'), 'lzma':
    ModuleVersionInfo('3.3', 'lzma', 'backports.lzma'), 'ipaddress':
    ModuleVersionInfo('3.4', 'ipaddress', 'py2-ipaddress'), 'enum':
    ModuleVersionInfo('3.4', 'enum', 'enum34'), 'typing': ModuleVersionInfo
    ('3.5', 'typing', 'typing'), 'secrets': ModuleVersionInfo('3.6',
    'secrets', 'python2-secrets'), 'statistics': ModuleVersionInfo('3.4',
    'statistics', 'statistics'), 'dataclasses': ModuleVersionInfo('3.7',
    'dataclasses', 'dataclasses'), 'contextvars': ModuleVersionInfo('3.7',
    'contextvars', 'contextvars')}


class NoUnusableImportsChecker(cb.CheckerBase):

    def __call__(self, ctx, tree):
        install_requires = ctx.cfg.install_requires
        target_version = ctx.cfg.target_version
        for node in ast.iter_child_nodes(tree):
            if not isinstance(node, (ast.Import, ast.ImportFrom)):
                continue
            module_names = []
            if isinstance(node, ast.Import):
                for alias in node.names:
                    module_names.append(alias.name)
            elif isinstance(node, ast.ImportFrom):
                module_name = node.module
                if module_name:
                    module_names.append(module_name)
            for mname in module_names:
                if mname not in MAYBE_UNUSABLE_MODULES:
                    continue
                vnfo = MAYBE_UNUSABLE_MODULES[mname]
                if target_version >= vnfo.available_since:
                    continue
                bppkg = vnfo.backport_package
                is_backported = vnfo.backport_package is not None
                is_backport_name_same = mname == vnfo.backport_module
                is_strict_mode = install_requires is not None
                is_whitelisted = (is_backport_name_same and 
                    install_requires is not None and bppkg in install_requires)
                if is_whitelisted:
                    continue
                is_hard_error = (not is_backported or is_strict_mode or not
                    is_backport_name_same)
                vnfo_msg = (
                    "This module is available since Python {0}, but you configured target_version='{1}'."
                    .format(vnfo.available_since, target_version))
                if is_hard_error:
                    errmsg = "Prohibited import '{0}'. {1}".format(mname,
                        vnfo_msg)
                    if bppkg:
                        errmsg += (
                            " Use 'https://pypi.org/project/{0}' instead.".
                            format(bppkg))
                    else:
                        errmsg += ' No backported for this package is known.'
                    raise common.CheckError(errmsg, node)
                else:
                    lineno = common.get_node_lineno(node)
                    loc = '{0}@{1}'.format(ctx.filepath, lineno)
                    log.warning("{0}: Use of import '{1}'. {2}".format(loc,
                        mname, vnfo_msg))
