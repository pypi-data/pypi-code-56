"""CORS Middleware."""

from ..helpers import config
from ..request import Request


class CorsMiddleware:
    """Appends CORS headers to HTTP response.

    Put any CORS middleware you need as a CORS dictionary inside your
    middleware config file.
    """

    def __init__(self, request: Request):
        """Inject Any Dependencies From The Service Container.

        Arguments:
            Request {masonite.request.Request} -- The Masonite request object
        """
        self.request = request

    def before(self):
        """Run This Middleware After The Route Executes."""
        headers = config('middleware.cors') or {}
        self.request.header(headers)
