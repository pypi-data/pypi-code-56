import logging
import json
import functools

from jsonschema import (
    validate, ValidationError, SchemaError, draft7_format_checker,
    Draft7Validator
)

from flask import current_app, request, Response

from .errors import *

logger = logging.getLogger(__name__)


class Schema(object):
    def __init__(self, app=None, cache=False):
        self.app = None
        self._validators = {}
        self._should_cache = cache
        if app is not None:
            self.app = app
            self.init_app(app)

    def init_app(self, app):
        # todo: read application configuration
        self.app = app or current_app

    def _get_validator(self, key, loader):
        if self._should_cache:
            v = self._validators.get(key)
            if v is not None:
                return v

        if not callable(loader):
            raise ValueError("schema_loader has to be callable")
        s = loader()
        v = Draft7Validator(schema=s, format_checker=draft7_format_checker)
        self._validators[key] = v
        return v

    @staticmethod
    def _validate(instance, schema):
        validate(instance, schema, format_checker=draft7_format_checker)

    def validate_response(self, instance, route_rule, method, loader):
        key = "response:%s:%s" % (method, route_rule)
        validator = self._get_validator(key, loader)
        try:
            validator.validate(instance)
        except ValidationError as e:
            self._re_raise(e, ResponseValidationError)
        except SchemaError as serr:
            logger.exception(serr)
            self._re_raise(serr, FlaskSchemaValidationError)

    def validate_request(self, instance, route_rule, method, loader):
        key = "request:%s:%s" % (method, route_rule)
        validator = self._get_validator(key, loader)
        try:
            # todo: implement the lazy lookup of errors
            # to get all the errors at once so it is possible
            # to return them to the error handler
            validator.validate(instance)
        except ValidationError as e:
            self._re_raise(e, RequestValidationError)
        except SchemaError as serr:
            logger.exception(serr)
            self._re_raise(serr, FlaskSchemaValidationError)

    @staticmethod
    def load_schema(path):
        logger.info("loading schema for: %s", path)
        _schema = None
        with open(path) as spec:
            _schema = json.loads(spec.read())
        return _schema

    def _re_raise(self, exc, _cls):
        # todo: process the error message in order to provide
        # more useful error details that can be configured.
        invalid = []
        required = []
        if exc.validator in ['type', 'format']:
            invalid = list(exc.path)
        elif exc.validator == 'required':
            required = list(exc.validator_value)

        raise _cls(exc.message, required, invalid)

    def check_request(self, schema_path):
        def loader():
            return self.load_schema(schema_path)

        def actual_decorator(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                # todo: get the payload from request
                payload = request.json
                self.validate_request(payload, request.url_rule, request.method, loader)
                return func(*args, **kwargs)

            return wrapper

        return actual_decorator

    def check_response(self, schema_path):
        def loader():
            return self.load_schema(schema_path)

        def actual_decorator(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                # execute handler
                resp = func(*args, **kwargs)
                payload = {}
                if isinstance(resp, Response):
                    payload = resp.json
                elif isinstance(resp, tuple):
                    payload = resp[0]
                else:
                    # assume it's a dict
                    payload = resp
                self.validate_response(payload, request.url_rule, request.method, loader)
                # if valid
                return payload

            return wrapper

        return actual_decorator
