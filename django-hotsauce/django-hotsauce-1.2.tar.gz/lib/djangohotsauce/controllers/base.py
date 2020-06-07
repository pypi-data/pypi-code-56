#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""BaseController CPython API Version 1.2 revision 0

Python extension module to implement MVC-style "controllers"
for Django and WSGI type apps. In short, ``BaseController`` derived
extensions are request handlers resolving a ``path_url`` string
to a matching ``view function``. The response handler (view function)
then resolve the appropriate HTTP response to the client.

TODO:
-Better module-level documentation (work-in-progress)
-Compatibility with mod_wsgi (Apache2) (YMMV...)
-Change all prints by log() hooks (work-in-progress)
-use signals to log messages from pubsub like BUS

Define and document the internal request handling stages when
using native Django views (WSGIHandler):
 __init__,         # application init -> self.init_request(env)
 init_request,     # setup the environment -> self.process_request(req)
 process_request,  # handle the request -> self.locals.request = req
 get_response,     # resolve request [PATH_INFO] -> response_callback
 application,      # response stage 2 [WSGI] -> response_callback(env, start_response)
"""

import sys
import os
import urllib
from contextlib import contextmanager
from djangohotsauce.utils.log import configure_logging
log = configure_logging(__name__)
from djangohotsauce.utils.wsgilib import (
    HTTPRequest, 
    HTTPResponse,
    #HTTPNotFound,
    #HTTPUnauthorized,
    #HTTPException
    )
from djangohotsauce.utils.wsgilib.exc import (
    HTTPNotFound, 
    HTTPUnauthorized, 
    HTTPException
    )

from djangohotsauce.utils.django_compat import NoReverseMatch

from werkzeug.local import Local, LocalProxy

RequestClass = HTTPRequest

_local = Local()
#local_manager = LocalManager([_local]) 

__all__ = ('BaseController', 'sessionmanager', 'get_current_request')


@contextmanager
def sessionmanager(request):
    _local.request = request
    yield
    _local.request = None

def get_current_request():
    try:
        return _local.request
    except AttributeError:
        raise TypeError("No request object for this thread")

_request = LocalProxy(lambda: get_current_request())

class BaseController(object):
    _debug = False
    _settings = None
    _request_class = None  #RequestClass
    _response_class = None #HTTPResponse
    _response = None
    _environ = {}

    def application(self, environ, start_response):
        """
        Override this to change the default request/response
        handling.

        This method is used for properly returning a WSGI response instance
        by calling ``get_response``.

        The latter does the grunt work of routing the request to the
        proper callable function or class.

        """
        req = self._request_class(environ)

        with sessionmanager(req):
            
            self._request = self.init_request(req)
            #if self.debug == True:
            #    assert _request == self.request, 'Invalid request object!'
            #    assert _request == get_current_request(), 'Request is not the current one!'
            try:
                self._response = self.get_response(request=self.request)

            except HTTPException as e:
                log.debug(e)
                raise
        return self._response(environ, start_response)

    def __call__(self, environ, start_response):
        return self.application(environ, start_response)
