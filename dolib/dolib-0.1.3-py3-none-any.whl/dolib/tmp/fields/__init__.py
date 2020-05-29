class Field:
    def __init__(
        self, name=None, null=False, default=None, api_name=None, help_text=""
    ):

        assert type(null) == bool, "null must be bool type"
        assert type(name) in (str, type(None)), "name must be str type"
        assert type(api_name) in (str, type(None)), "api_name must be str type"
        assert type(help_text) == str, "help_text must be str type"

        self.name = name
        self.null = null
        self.default = default
        self.api_name = api_name
        self.help_text = help_text

    def to_python(self, value):
        return value


class BooleanField(Field):
    def to_python(self, value):
        if self.null and value is None:
            return None
        if value in (True, False):
            return bool(value)
        if value in ("t", "True", "1"):
            return True
        if value in ("f", "False", "0"):
            return False
        raise ValueError("Invalid value")


class IntegerField(Field):
    def to_python(self, value):
        if self.null and value is None:
            return None
        return int(value)


class StringField(Field):
    def to_python(self, value):
        if self.null and value is None:
            return None
        return str(value)
