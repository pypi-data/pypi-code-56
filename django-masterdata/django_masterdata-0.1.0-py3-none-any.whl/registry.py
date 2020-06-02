from collections import UserDict
from .modelregistry import ModelRegistry


class Registry(UserDict):
    def register(self, model):
        r = ModelRegistry(model)
        self[model] = r
        return r
