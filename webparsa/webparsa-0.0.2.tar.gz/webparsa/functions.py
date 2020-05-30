import builtins
from . import thread_locals

default_functions = {
    "remove_commas": lambda x: x.replace(",", ""),
}

def runFunction(fnName, value):
    if fnName.startswith("."):
        return getattr(value, fnName[1:])()
    else:
        if fnName in thread_locals.parsa_functions:
            return thread_locals.parsa_functions[fnName](value)
        elif fnName in default_functions:
            function = default_functions[fnName];
            return function(value)
        elif fnName in dir(builtins):
            function = getattr(builtins, fnName)
            return function(value)
        else:
            raise ValueError(f"Function not found - {fnName}")
