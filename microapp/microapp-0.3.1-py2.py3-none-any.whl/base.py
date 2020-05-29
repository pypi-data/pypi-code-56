# -*- coding: utf-8 -*-
"""Microapp basic object module"""

import sys, abc


#exclude_list = ["exec", "eval", "breakpoint", "delattr", "setattr",
#                "globals", "input", "locals", "memoryview", "object",
#                "open", "print", "super", "type", "vars", "__import__"]

exclude_list = ["exec", "eval", "breakpoint", "memoryview"]

microapp_builtins = dict((k, v) for k, v in __builtins__.items()
                       if k not in exclude_list)


if sys.version_info >= (3, 0):
    Object = abc.ABCMeta("Object", (object,), {})

else:
    Object = abc.ABCMeta("Object".encode("utf-8"), (object,), {})

class MicroappObject(Object):
#class MicroappObject(metaclass=abc.ABCMeta):

    #def __new__(meta, name, bases, dct):
    #    add builtin configurations
    #    return super(_MicroappObject, meta).__new__(meta, name, bases, dct)

    @property
    @abc.abstractmethod
    def _name_(self):
        pass

    @property
    @abc.abstractmethod
    def _version_(self):
        pass

del exclude_list
