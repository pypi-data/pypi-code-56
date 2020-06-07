#!/usr/bin/env python
# -*- coding: utf-8 -*-

from djangohotsauce.controllers.wsgi import WSGIController
from djangohotsauce.utils.log import configure_logging
log = configure_logging('OAuthController')

try:
    from djangohotsauce.oauthclient import (
        OAuthClient,
        OAuthResponseMiddleware,
        google
        )
except ImportError:        
    from wsgi_oauth2.client import OAuthClient 
    from wsgi_oauth2.controller import OAuthResponseMiddleware
    from wsgi_oauth2.provider import google

__all__ = ['OAuthController']

class OAuthController(WSGIController):

    def __init__(self, client=None, **kwargs):
        super(OAuthController, self).__init__(**kwargs)
        if client is not None:
            self._client = client
        else:
            self._client = OAuthClient(
                google,
                self.settings.OAUTH2_CLIENT_ID,
                self.settings.OAUTH2_ACCESS_TOKEN,
                self.settings.OAUTH2_SCOPE, 
                self.settings.OAUTH2_REDIRECT_URL,
            )

    def __call__(self, environ, start_response):
        client = self._client
        callback = object().__new__(OAuthResponseMiddleware)
        callback.__init__(self, client)
        environ.update(callback._environ)
        return self.application(environ, start_response)
        
