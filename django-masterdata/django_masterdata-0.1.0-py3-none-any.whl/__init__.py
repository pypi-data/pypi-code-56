from .check import Check
from .registry import Registry


def register(*args, **kwargs):
    return default_registry.register(*args, **kwargs)


default_registry = Registry()
