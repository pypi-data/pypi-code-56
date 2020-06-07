#!/usr/bin/env python
# -*- coding: utf-8 -*-
import traceback

from importlib import import_module

from djangohotsauce.controllers.base import BaseController
from djangohotsauce.utils.django_settings import LazySettings
from djangohotsauce.utils.django_compat import get_resolver
from djangohotsauce.utils.django_compat import NoReverseMatch
from djangohotsauce.utils.log import configure_logging
log = configure_logging(__name__)
from djangohotsauce.utils.wsgilib import (
    HTTPRequest, 
    HTTPResponse,
    HTTPNotFound,
    HTTPUnauthorized,
    #HTTPAuthenticationError,
    HTTPException
    )

#try:
#    import django
#    django.setup()
#except:
#    log.debug("Django apps registry disabled!") 
#    pass

try:
    from authkit.permissions import NotAuthenticatedError    
except ImportError:
    log.debug("Please install libauthkit!")
    class NotAuthenticatedError(HTTPException):
        pass


__all__ = ('WSGIController',)

class WSGIController(BaseController):

    _request_class = HTTPRequest
    _response_class = HTTPResponse

    def __init__(self, settings=None, enable_logging=True, 
        autoload=True, debug=False):
        """
        Initializes a ``BaseController`` instance for processing
        standard Django view functions and handling basic error conditions.

        Available keyword arguments:

        - ``settings``: Django settings module (required)
        """
        if settings is not None:
            self.settings = settings
        else:
            self.settings = LazySettings()

        # If using legacy autoload mecanism, attempt to register user-specified
        # wsgi callbacks. (DEPRECATED)
        #if (autoload and hasattr(self.settings, 'CUSTOM_ERROR_HANDLERS')):
        #    self.registerWSGIHandlers(self.settings.CUSTOM_ERROR_HANDLERS)

        setattr(self, 'urlconf', self.settings.ROOT_URLCONF)
        setattr(self, 'resolver', get_resolver(self.urlconf, self.settings))
        self.resolver._urlconf_module = import_module(self.urlconf)
        if enable_logging:
            log.debug("Logging support initialized")
            self.logger = log
            
    def get_response(self, request):
        """Process ``path_url`` and return a callable function as
        the WSGI ``response`` callback.

        The callback view function is resolved using the built-in
        Django ``RegexURLResolver`` class.

        Returns a callable function (Response) or None if no
        view functions matched.

        See the docs in :djangohotsauce.utils.django_compat.RegexURLResolver:
        for details.

        This function may be overrided in custom subclasses to modify
        the response type.
        """

        # Resolve the path (endpoint) to a view using legacy Django URL
        # resolver.
        try:
            #Match the location to a view or callable
            path_info = self._get_path_info(request.environ)
            (callback, args, kwargs) = self.resolver.resolve(path_info)
            # Create the wsgi ``response`` object.
            response = callback(request, *args, **kwargs)
        except NoReverseMatch:
            # Handle 404 responses with a custom 404 handler.
            request.environ['django.debug.error_message'] = \
                        'Page not found'
            return self.error(request, 404)
        except (HTTPUnauthorized, NotAuthenticatedError):
            # XXX redirect to /oauth2callback?=path_url for authorization
            # with google oauth
            if self.debug:
                self.logger.debug("Caught authorization exception!")
                error_message = traceback.format_exc()
                request.environ['django.debug.error_message'] = \
                        error_message
            #User signin redirect            
            return self.error(request, 403, next='/session_login/')
        except HTTPException:
            request.environ['django.debug.error_message'] = \
                traceback.format_exc()
            return self.error(request, 500)
        return response

    def init_request(self, request):
        """A method to execute before ``process_request``"""
        # put handle404 and handle500 in request.environ
        if hasattr(self, 'handle404'):
            request.environ['django.request.handle404'] = self.handle404
        if hasattr(self, 'handle500'):
            request.environ['django.request.handle500'] = self.handle500
        if hasattr(self, 'settings'):
            request.environ['django.settings'] = self.settings
        return request
    
    @property
    def request(self):
        return self._request

    @property
    def response(self):
        return self._response

    @property
    def user(self):
        return self.request.get_user()

    def _environ_getter(self):
        """ Returns the current WSGI environment instance."""
        return getattr(self, '_environ', {})

    environ = property(_environ_getter)

    def _method_getter(self):
        return self.environ['REQUEST_METHOD']
    method = property(_method_getter)

    def _debug_getter(self):
        """Global debug flag. 
        Set settings.DEBUG to False to disable debugging"""
        return bool(self.settings.DEBUG == True)
    debug = property(_debug_getter)

    def _get_path_info(self, env):
        return str(env.get('PATH_INFO', ''))

