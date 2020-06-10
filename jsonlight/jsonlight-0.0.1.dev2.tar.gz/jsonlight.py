import json
from pathlib import Path
from datetime import datetime
from uuid import UUID


def strdump(self):
    return str(self)


@classmethod
def strload(cls, data):
    return cls(data)


for patch in (UUID, Path):
    patch.__jsondump__ = strdump
    patch.__jsonload__ = strload


# monkey patching that one is prevented by Python
class datetime(datetime):  # noqa
    def __jsondump__(self):
        return self.isoformat()

    @classmethod
    def __jsonload__(cls, data):
        return cls.fromisoformat(data)


class JSONMixin:
    def __jsondump__(self):
        if hasattr(self, '__getstate__'):
            return dump(self.__getstate__())

    @classmethod
    def __jsonload__(cls, data):
        if hasattr(cls, '__setstate__'):
            return cls.__setstate__(data)
        return cls(**data)


def dump(obj):
    if hasattr(obj, '__jsondump__'):
        obj = obj.__jsondump__()

    if isinstance(obj, dict):
        obj = {key: dump(value) for key, value in obj.items()}
    elif isinstance(obj, list):
        obj = [dump(value) for value in obj]

    return obj


def dumps(obj):
    return json.dumps(dump(obj))


def load(cls, data):
    if hasattr(cls, '__jsonload__'):
        return cls.__jsonload__(data)
    return data


def loads(cls, data):
    data = json.loads(data)
    return load(cls, data)
