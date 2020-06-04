import ast
import importlib
import inspect
import sys
from textwrap import dedent
from types import CodeType, FunctionType

import dill


def parse_object(obj):
    source = getattr(obj, '__inject_code__', dill.source.getsource(obj))
    for _ in range(5):
        try:
            return ast.parse(source)
        except IndentationError:
            source = dedent(source)


# unused
def find_nested_func(parent, child_name):
    """Return the function named <child_name> that is defined inside a <parent>
    function.

    Returns None if nonexistent.
    """
    consts = parent.__code__.co_consts
    for item in consts:
        if isinstance(item, CodeType) and item.co_name == child_name:
            return FunctionType(item, globals())


# unused
def import_code(module, code):
    """Code can be any object containing code -- string, file obj, or compiled
    code object. Returns a new module initialized by dynamically importing the
    given code and adds it to sys.modules under the given module's name.
    """
    mod_file = dill.source.getfile(module)
    exec(compile(code, mod_file, 'exec', dont_inherit=True), vars(module))

    name = dill.source.getname(module)
    sys.modules[name] = module
    globals()[name] = module
    importlib.invalidate_caches()
    return module


def get_class_that_defined_method(meth):
    if dill.source.ismethod(meth):
        for cls in inspect.getmro(meth.__self__.__class__):
            if cls.__dict__.get(meth.__name__) is meth:
                return cls
        meth = meth.__func__  # fallback to __qualname__ parsing
    if dill.source.isfunction(meth):
        class_name = meth.__qualname__.split('.<locals>', 1)[0].rsplit('.', 1)[0]
        try:
            cls = getattr(dill.source.getmodule(meth), class_name)
        except AttributeError:
            cls = meth.__globals__.get(class_name)
        if isinstance(cls, type):
            return cls
    return getattr(meth, '__objclass__', None)  # handle special descriptor objects


def tryattrs(obj, *attrs):
    for attr in attrs:
        try:
            return getattr(obj, attr)
        except AttributeError:
            pass
    obj_name = dill.source.getname(obj)
    raise AttributeError("'{}' object has no attribute in {}", obj_name, attrs)
