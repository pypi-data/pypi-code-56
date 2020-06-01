import traceback
from functools import wraps
from logging import getLogger
from typing import Type, Optional, Union, Callable, Tuple

from flask import request, jsonify
from marshmallow import Schema
from marshmallow import ValidationError
from werkzeug import Response, exceptions  # noqa: PyPackageRequirements

from avatar_utils.core import create_response
from avatar_utils.validation.constants import ServiceHTTPMethods, ServiceHTTPCodes

logger = getLogger(__name__)


def validate_json(request_schema: Optional[Type[Schema]] = None,
                  response_schema: Optional[Type[Schema]] = None,
                  method: Union[str, ServiceHTTPMethods] = ServiceHTTPMethods.GET) -> Callable:

    method = method.name if isinstance(method, ServiceHTTPMethods) else method.upper()

    def decorator(f) -> Callable:

        @wraps(f)
        def wrapper(*args, **kw) -> Union[str, Tuple[Response, int]]:

            log_prefix = f'[ VALIDATION | {request.remote_addr} {request.method} > {request.url_rule} ]'

            # skip decorator if unexpected HTTP method of request
            if method != request.method:
                logger.debug(f'{log_prefix} skip {request.method} method, validator expect {method}')
                return f(*args, **kw)

            # validate request data
            if request_schema:
                validation_schema = request_schema()

                if not request.is_json:
                    logger.warning(f'{log_prefix} < invalid content-type header')
                    return create_response(status=ServiceHTTPCodes.BAD_REQUEST.value,
                                           message='invalid content-type header')
                try:
                    validation_schema.load(request.json)
                    logger.debug(f'{log_prefix} request body validated')
                except exceptions.BadRequest:
                    logger.warning(f'{log_prefix} < invalid requests body')
                    return create_response(status=ServiceHTTPCodes.BAD_REQUEST.value,
                                           message='invalid requests body')
                except ValidationError as err:
                    logger.warning(f'{log_prefix} < validation error')
                    return create_response(status=ServiceHTTPCodes.UNPROCESSABLE_ENTITY.value,
                                           message='validation error',
                                           data=dict(err.messages))
            # call HTTP handler
            try:
                result = f(*args, **kw)
                if isinstance(result, Response):
                    result = create_response(data=result.json,
                                             status=result.status_code)
                response, status = result if isinstance(result, tuple) else create_response(result)
            except Exception as err:  # noqa
                logger.error(f'{log_prefix} < {err}')
                response, status = create_response(status=ServiceHTTPCodes.SERVER_ERROR.value,
                                                   message='unhandled error',
                                                   data=dict(
                                                       error=type(err).__name__,
                                                       traceback=str(traceback.format_exc())
                                                   ))
                return response, status

            # validate response data
            if response_schema:
                validation_schema = response_schema()

                if response.status_code != ServiceHTTPCodes.OK.value:
                    return response, status

                try:
                    data = validation_schema.load(response.json)
                    logger.debug(f'{log_prefix} response validated')
                    response = jsonify(validation_schema.dump(data))
                except (exceptions.BadRequest, ValidationError, TypeError) as err:
                    logger.error(f'{log_prefix} < {err}')
                    response, status = create_response(status=ServiceHTTPCodes.SERVER_ERROR.value,
                                                       message='incorrect response data',
                                                       data=dict(
                                                           error=type(err).__name__,
                                                           traceback=str(traceback.format_exc())
                                                       ))
                finally:
                    return response, status

            return response, status
        return wrapper

    return decorator
