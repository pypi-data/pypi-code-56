import functools
from typing import Callable

from jeffy.encoding import Encoding
from jeffy.encoding.bytes import BytesEncoding
from jeffy.sdk.s3 import S3
from jeffy.validator import NoneValidator, Validator


class S3HandlerMixin(object):
    """S3 event handler decorators."""

    def s3(
        self,
        encoding: Encoding = BytesEncoding(),
        validator: Validator = NoneValidator()
    ) -> Callable:
        """
        Decorator for S3 event.

        Automatically parse object body stream to Lambda.

        Usage::
            >>> from jeffy.framework import setup
            >>> from jeffy.encoding.bytes import BytesEncoding
            >>> app = get_app()
            >>> @app.handlers.s3(encoding=BytesEncoding())
            ... def handler(event, context):
            ...     return event['body']
        """
        def _s3(func: Callable) -> Callable:  # type: ignore
            @functools.wraps(func)
            def wrapper(event, context):            # type: ignore
                ret = []
                for record in event['Records']:
                    bucket = record['s3']['bucket']['name']
                    key = record['s3']['object']['key']
                    try:
                        response = S3().get_resource().get_object(Bucket=bucket, Key=key)
                        self.capture_correlation_id(response['Metadata'])
                        body = encoding.decode(response['Body'].read())
                        validator.validate(body)
                        ret.append(func({
                            'key': key,
                            'bucket_name': bucket,
                            'body': body,
                            'metadata': response['Metadata']
                        }, context))
                    except Exception as e:
                        self.app.logger.exception(e)
                        raise e
                return ret
            return wrapper
        return _s3
