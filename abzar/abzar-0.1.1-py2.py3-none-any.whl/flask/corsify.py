import re
from typing import List, Pattern

from flask import Request, Response


def cors_handler(
    request: Request, response: Response, whitelist: List[Pattern], allowed_headers: List[str] = None
) -> Response:
    if not allowed_headers:
        allowed_headers = []
    # CORS handling
    client_origin = request.headers.get("Origin", None)
    for pattern in whitelist:
        if client_origin and re.match(pattern, client_origin):
            response.headers["Access-Control-Allow-Origin"] = client_origin
            # To be able to accept cookie
            response.headers["Access-Control-Allow-Credentials"] = "true"
            response.headers["Access-Control-Allow-Headers"] = f'Authorization, {", ".join(allowed_headers)}'
            response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS, PATCH"
            break
    return response


class Corsify:
    def __init__(self, app):
        self.app = app.wsgi_app
        app.wsgi_app = self

    def __call__(self, environ, start_response):
        # Not yet Flask world, we have to push the context first when we do from_app down below
        current_request = Request(environ)
        # wsgi -> flask world
        response = Response.from_app(self.app, environ, buffered=True)
        response = cors_handler(current_request, response)

        # and now back to wsgi
        app_iter, status, headers = response.get_wsgi_response(environ)
        start_response(status, headers)
        return app_iter
