class Response:
    """Response object.

    Attributes:
        _http_code (constants.enums.HttpCode):
            Guarantee valid code. Default HttpCode.OK.
        message (str): A message.
        errors (list): List of errors.

    Examples:
        Instantiate class.

        >>> r = Response(http_code=200, message='OK')
        >>> r.message
        'OK'
    """

    def __init__(
        self,
        http_code: int = None,
        message: str = None,
        error: (dict, list) = None,
        data: (dict, list) = None
    ):

        self.http_code = http_code
        self.message = message
        self.error = error
        self.data = data

    def __json__(self):
        return {
            'http_code': self.http_code,
            'message': self.message,
            'error': self.error,
            'data': self.data
        }
