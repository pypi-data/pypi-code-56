class Representable:
    def __repr__(self):
        attrs = ", ".join("{}:{!r}".format(k, v) for k, v in vars(self).items())

        return "<{} {}>".format(type(self).__name__, attrs)
