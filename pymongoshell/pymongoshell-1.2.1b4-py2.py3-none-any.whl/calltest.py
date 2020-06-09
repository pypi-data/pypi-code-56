class CallTest:

    def __init__(self, name):
        print("make CallTest")
        self._name = name

    def dummy(self):
        print("dummy")

    def __call__(self):
        print("__call__")

    def __getattr__(self, name):
        print(f"__getattr__ {name}")
        return self.__getitem__("_getattr__.__getitem__")

    def __getitem__(self, item):
        print(f"__getitem__")
        return CallTest("__getitem__")

    def __repr__(self):
        return f"CallTest({self._name})"


print(">> x=CallTest('first')")
x= CallTest("first")

print(">> x.dummy()")
x.dummy()
print(">> x.mummy()")
x.mummy()
