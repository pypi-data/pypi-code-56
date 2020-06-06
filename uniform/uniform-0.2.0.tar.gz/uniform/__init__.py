from typing import Callable, Optional, Type

from starlette import status
from starlette.requests import Request
from starlette.responses import JSONResponse, Response
from typesystem import Message, Schema, ValidationError
from typesystem.base import ValidationResult


class Uniform:
    def __init__(self, schema: Type[Schema]) -> None:
        self.schema = schema

    async def validate(self, request: Request) -> ValidationResult:
        data = None  # type: Optional[dict]
        content_type = request.headers.get("Content-Type")
        if content_type == "application/x-www-form-urlencoded":
            form = await request.form()
            data = dict(form)
        elif content_type == "application/json":
            data = await request.json()
        else:
            return ValidationResult(
                value=None,
                error=ValidationError(
                    messages=[
                        Message(
                            text="Invalid Content-Type value.",
                            code="invalid",
                            index=["content_type"],
                        )
                    ]
                ),
            )

        return self.schema.validate_or_error(data)


def validate(uniform: Uniform) -> Callable:
    def outer_wrapper(endpoint: Callable) -> Callable:
        async def endpoint_wrapper(request: Request) -> Response:
            data, errors = await uniform.validate(request)
            if errors:
                return JSONResponse(
                    content={
                        "ok": False,
                        "description": "Bad Request, Schema Validation Failed.",
                        "result": dict(errors),
                    },
                    status_code=status.HTTP_400_BAD_REQUEST,
                )

            request.state.data = data
            return await endpoint(request)

        return endpoint_wrapper

    return outer_wrapper
