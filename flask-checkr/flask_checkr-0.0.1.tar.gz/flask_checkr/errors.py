class FlaskSchemaValidationError(Exception):
    def __init__(self, message, required, invalid):
        self.message = message
        self.required = required
        self.invalid = invalid

    def to_dict(self):
        return {
            "message": self.message,
            "required": self.required,
            "invalid": self.invalid,
        }


class ResponseValidationError(FlaskSchemaValidationError):
    def __init__(self, *args, **kwargs):
        super(ResponseValidationError, self).__init__(*args, **kwargs)


class RequestValidationError(FlaskSchemaValidationError):
    def __init__(self, *args, **kwargs):
        super(RequestValidationError, self).__init__(*args, **kwargs)
