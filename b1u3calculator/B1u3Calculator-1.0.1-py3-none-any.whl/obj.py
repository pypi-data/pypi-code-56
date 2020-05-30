
class Object:
    def __init__(self, **kwargs):
        for k in kwargs:
            assert type(k) == str
            setattr(self, k, kwargs[k])

    def type(self):
        raise NotImplementedError()

    def inspect(self):
        """ String when this object is evaluated """
        raise NotImplementedError()

""" object type name """
INTEGER = "INTEGER_OBJ"

class Integer(Object):
    value = 0

    def type(self):
        return INTEGER

    def inspect(self):
        return str(self.value)

RETURN = "RETURN_OBJ"

class Return(Integer):
    value = Integer(value=0)

    def type(self):
        return RETURN

