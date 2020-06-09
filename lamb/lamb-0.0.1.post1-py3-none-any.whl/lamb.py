# Copyright (c) 2020 Silas Gyger

import sys
import types
import string

import importlib.machinery as imach
import importlib.util as iutil
import importlib.abc as iabc

class _LambdaFactory:
    def __init__(self, chain=[lambda x: x]):
        self.__chain = chain
    
    def __enchain(self, fun):
        return _LambdaFactory(self.__chain + [fun])

    def __call__(self, *args):
        argc = len(args)
        if argc == 0:
            return self.__enchain(lambda x: x())
        elif argc == 1:
            arg = args[0]
            for f in self.__chain:
                arg = f(arg)
            return arg
        else:
            f = self
            for arg in args:
                f = f(arg)
            return f

    def __getattr__(self, name):
        return self.__enchain(lambda a: getattr(a, name))
    
    def __getitem__(self, b):
        return self.__enchain(lambda a: a[b])

    # Comparators

    def __lt__(self, b):
        return self.__enchain(lambda o: o < b)
    
    def __le__(self, b):
        return self.__enchain(lambda o: o <= b)
    
    def __eq__(self, b):
        return self.__enchain(lambda o: o == b)
    
    def __ne__(self, b):
        return self.__enchain(lambda o: o != b)

    def __gt__(self, b):
        return self.__enchain(lambda o: o > b)
    
    def __ge__(self, b):
        return self.__enchain(lambda o: o >= b)

    # Operators

    def __add__(self, b):
        return self.__enchain(lambda a: a + b)
    
    def __sub__(self, b):
        return self.__enchain(lambda a: a - b)
    
    def __mul__(self, b):
        return self.__enchain(lambda a: a * b)
    
    def __matmul__(self, b):
        return self.__enchain(lambda a: a @ b)
    
    def __truediv__(self, b):
        return self.__enchain(lambda a: a / b)
    
    def __floordiv__(self, b):
        return self.__enchain(lambda a: a // b)
    
    def __mod__(self, b):
        return self.__enchain(lambda a: a % b)
    
    def __pow__(self, b):
        return self.__enchain(lambda a: a ** b)
    
    def __lshift__(self, b):
        return self.__enchain(lambda a: a << b)
    
    def __rshift__(self, b):
        if callable(b):
            return self.__enchain(lambda a: b(a))
        else:
            return self.__enchain(lambda a: a >> b)
    
    def __and__(self, b):
        return self.__enchain(lambda a: a & b)
    
    def __xor__(self, b):
        return self.__enchain(lambda a: a ^ b)
    
    def __or__(self, b):
        return self.__enchain(lambda a: a | b)
    
    # Mirrored operators
    
    def __radd__(self, a):
        return self.__enchain(lambda b: a + b)

    def __rsub__(self, a):
        return self.__enchain(lambda b: a - b)

    def __rmul__(self, a):
        return self.__enchain(lambda b: a * b)

    def __rmatmul__(self, a):
        return self.__enchain(lambda b: a @ b)

    def __rtruediv__(self, a):
        return self.__enchain(lambda b: a / b)

    def __rfloordiv__(self, a):
        return self.__enchain(lambda b: a // b)

    def __rmod__(self, a):
        return self.__enchain(lambda b: a % b)

    def __rpow__(self, a):
        return self.__enchain(lambda b: a ** b)

    def __rlshift__(self, a):
        return self.__enchain(lambda b: a << b)

    def __rrshift__(self, a):
        return self.__enchain(lambda b: a >> b)

    def __rand__(self, a):
        return self.__enchain(lambda b: a & b)

    def __rxor__(self, a):
        return self.__enchain(lambda b: a ^ b)

    def __ror__(self, a):
        return self.__enchain(lambda b: a | b)
    
    # Representations

    def __repr__(self):
        return f"<LambdaFactory | functions: {self.__chain}>"

    def __str__(self):
        return '🐑'


lamb = _LambdaFactory()

# Create dynamic lamb names with post- and prefixes
class _DynamicLambGenerator(types.ModuleType):
    __varnames = string.ascii_lowercase

    def __init__(self, prefix, suffix):
        super().__init__(name="varname_generation")
        self.__all__ = list(map(
            prefix + lamb + suffix,
            self.__varnames
        ))

    def __getattr__(self, name):
        if name in self.__all__:
            return lamb  # 🐑
        else:
            raise AttributeError


class _DynamicLambMetaPathFinder(iabc.MetaPathFinder):
    base_name = "vs"

    def find_spec(self, fullname, path, target=None):
        modname = fullname.split(".")[-1]
        if self.base_name in modname:
            prefix, suffix = modname.split(self.base_name, 1)
            return imach.ModuleSpec(
                name=fullname,
                loader=_DynamicLambLoader(prefix, suffix)
            )


class _DynamicLambLoader:
    def __init__(self, prefix, suffix):
        self.p, self.s = prefix, suffix

    def exec_module(self, spec):
        pass

    def create_module(self, spec):
        return _DynamicLambGenerator(self.p, self.s)


# Make module to a package
__path__ = []
# Make all packages containing "vs" discoverable
sys.meta_path.append(_DynamicLambMetaPathFinder())
