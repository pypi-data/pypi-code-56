from . import fields


class BaseModel:
    def __init__(self, *args, **kwargs):
        self._fields = []

        for attr in self.__dir__():
            if issubclass(type(getattr(self, attr)), fields.Field):
                self._fields.append(attr)

        # set to default values from Field
        for field in self._fields:
            setattr(self, field, getattr(self, field).default)

        # set values from args
        for value, field in zip(args, self._fields):
            setattr(self, field, value)
            kwargs.pop(field, None)

        # set values from kwargs
        for key in kwargs:
            if key not in self._fields:
                continue
            setattr(self, key, kwargs.get(key))

    @classmethod
    def fields(cls):
        result = set()
        for attr in dir(cls):
            if issubclass(type(getattr(cls, attr)), fields.Field):
                result.add(attr)

        return result
