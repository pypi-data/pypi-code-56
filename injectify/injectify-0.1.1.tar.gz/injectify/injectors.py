"""
injectify.injectors
~~~~~~~~~~~~~~~~~

This module contains the model objects that power Injectify.
"""

import ast
from abc import ABC, abstractmethod
from collections import defaultdict
from functools import wraps

import astunparse
import dill

from .structures import listify
from .utils import parse_object, tryattrs, get_class_that_defined_method


def count_visit(f):
    @wraps(f)
    def wrapper(self, node):
        if f.__name__ not in self._visit_counter:
            # B/c increment happens before function call,
            # initialize at -1
            self._visit_counter[f.__name__] = -1

        self._visit_counter[f.__name__] += 1
        r = f(self, node, self._visit_counter[f.__name__])
        return r
    return wrapper


class BaseInjector(ABC, ast.NodeTransformer):
    handler = None

    def __init__(self, save_state=True):
        #: bool, if target object should allow multiple injections
        self.save_state = save_state

        self._visit_counter = defaultdict(int)

    def prepare(self, target, handler):
        self.prepare_target(target)
        self.prepare_handler(handler)

    @staticmethod
    def caninject(obj):
        """Return true if code can be injected into object."""
        return not (dill.source.ismodule(obj)
                    or dill.source.isclass(obj)
                    or dill.source.ismethod(obj)
                    or dill.source.isfunction(obj))

    def prepare_target(self, target):
        if self.caninject(target):
            raise TypeError('cannot inject to type {!r}', type(target))
        self.target = target

    def prepare_handler(self, handler):
        node = parse_object(handler)
        self.handler = node.body[0].body

    def visit_target(self):
        return self.visit(parse_object(self.target))

    def is_target_module(self):
        return dill.source.ismodule(self.target)

    def compile(self, tree):
        target_name = dill.source.getname(self.target)
        target_file = dill.source.getfile(self.target)
        target_src = dill.source.getsource(self.target)

        node = next(x for x in tree.body if getattr(x, 'name', None) == target_name)
        code = astunparse.unparse(node)

        _locals = {}
        exec(compile(code, target_file, 'exec', dont_inherit=True), {},  _locals)
        compiled_func = _locals[target_name]

        try:
            # Used to allow injection multiple times in a
            # single object, b/c inject.findsource() reads
            # the actual source file
            self.target.__inject_code__ = code if self.save_state else target_src

            # If function has code object, simply replace it
            self.target.__code__ = compiled_func.__code__
        except AttributeError:
            # Attempt to the class that the function is defined in
            meth_mod = get_class_that_defined_method(self.target)
            if not meth_mod:
                # If function is not defined in a class, or the target is not a function
                meth_mod = dill.source.getmodule(self.target)

            if self.save_state:
                # Used to allow injection multiple times in a
                # single object, b/c inject.findsource() reads
                # the actual source file
                compiled_func.__inject_code__ = code

            setattr(meth_mod, target_name, compiled_func)

    @abstractmethod
    def inject(self, node):
        pass


class HeadInjector(BaseInjector):

    def visit_Module(self, node):
        # Since ``Module`` node is always the top node
        # but we may not want to inject into the module
        if self.is_target_module():
            return self._visit(node)
        self.generic_visit(node)
        return node

    def visit_ClassDef(self, node):
        return self._visit(node)

    def visit_FunctionDef(self, node):
        return self._visit(node)

    def _visit(self, node):
        return ast.fix_missing_locations(self.inject(node))

    def inject(self, node):
        node.body.insert(0, self.handler)
        return node


class TailInjector(BaseInjector):

    def visit_Module(self, node):
        # Since ``Module`` node is always the top node
        # but we may not want to inject into the module
        if self.is_target_module():
            return self._visit(node)
        self.generic_visit(node)
        return node

    def visit_ClassDef(self, node):
        return self._visit(node)

    def visit_FunctionDef(self, node):
        return self._visit(node)

    def _visit(self, node):
        return ast.fix_missing_locations(self.inject(node))

    def inject(self, node):
        node.body.append(self.handler)
        return node


class ReturnInjector(BaseInjector):

    def __init__(self, ordinal=None, *args, **kwargs):
        #: zero-based index to choose specific target
        self.ordinal = listify(ordinal)

        super().__init__(*args, **kwargs)

    @count_visit
    def visit_Return(self, node, visit_count):
        print(visit_count)
        if (not self.ordinal or visit_count in self.ordinal):
            return ast.copy_location(self.inject(node), node)
        self.generic_visit(node)
        return node

    def inject(self, node):
        return ast.Module(body=[self.handler, node])


class FieldInjector(BaseInjector):

    def __init__(self, field, ordinal=None, insert=None, *args, **kwargs):
        #: the field to inject at
        self.field = field
        #: zero-based index to choose specific target
        self.ordinal = listify(ordinal)
        #: where to insert the handler's code relative to target
        self.insert = insert

        self._field_counter = defaultdict(int)

        super().__init__(*args, **kwargs)

    def visit_Assign(self, node):
        field = self.field or self.target

        if any(field == tryattrs(t, 'id', 'attr') for t in node.targets):
            field_count = self._field_counter[field]
            self._field_counter[field] += 1
            if (not self.ordinal or field_count in self.ordinal):
                return ast.copy_location(self.inject(node), node)
        self.generic_visit(node)
        return node

    def inject(self, node):
        if self.insert == 'after':
            return ast.Module(body=[node, self.handler])
        else:
            return ast.Module(body=[self.handler, node])


class NestedInjector(BaseInjector):

    def __init__(self, nested, injector, *args, **kwargs):
        #: name of the nested function
        self.nested = nested
        #: injector to use in the nested function
        self.injector = injector

        super().__init__(*args, **kwargs)

    def prepare(self, target, handler):
        super().prepare(target, handler)
        self.injector.prepare(target, handler)

    def visit_FunctionDef(self, node):
        if node.name == self.nested:
            return ast.fix_missing_locations(self.inject(node))
        self.generic_visit(node)
        return node

    def inject(self, node):
        return self.injector.inject(node)
