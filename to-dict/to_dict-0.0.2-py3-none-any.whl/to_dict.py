from enum import Enum

class Dictable:
    @property
    def dict(self):
        d = {}

        for k, v in self.__dict__.items():
            if issubclass(type(v), Dictable):
                v = v.dict
            elif issubclass(type(v), Enum):
                v = v.value

            d[k] = v

        return d