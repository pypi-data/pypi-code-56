from __future__ import annotations

import sys

from pydantic import BaseModel as Schema

from zealous import exceptions


__all__ = (
    "ErrorSchema",
    "Schema",
)


class NoExceptionCurrentlyBeingHandled(exceptions.BaseError):
    message = "No exception is currently being handled."


class ErrorSchema(Schema):
    type: str
    message: str

    @classmethod
    def from_exc_info(cls) -> ErrorSchema:
        """Generate error for the exception that is currently being handled."""
        type_, value, _ = sys.exc_info()
        if type_ and value:
            return cls(type=type_.__name__, message=str(value))
        raise NoExceptionCurrentlyBeingHandled
