#!/usr/bin/env python
# -*- coding: utf-8 -*-

from djangohotsauce.controllers.base import BaseController
from djangohotsauce.dbapi.orm import ClientStorageProxy
from djangohotsauce.utils.log import configure_logging

__all__ = ['ZODBController']

class ZODBController(BaseController):

    schevo_key_prefix = 'schevo.db.'
    zodb_debug = True
    zodb_backend_class = ClientStorageProxy
    logger = configure_logging('ZODBController')

    def __init__(self, request, db_name, manager=None, **kwargs):
        super(ZODBController, self).__init__(**kwargs)
        self.environ_key = str(self.schevo_key_prefix + 'zodb')
        self.manager = manager
        self.setup_database(db_name)
        
    def setup_database(self, db_name):
        if self.manager is None:
            #raise ValueError("Database manager is not set!")
            #Backward-compatible mode!

            self.db = self.zodb_backend_class(db_name)
        else:
            try:
                #print self.manager.connections
                self.db = self.manager[db_name]
                if self.debug:
                    assert self.db is not None
            except (KeyError, AttributeError):
                raise
        if self.zodb_debug:
            self.logger.debug("Configured database: %s" % self.db)
        return None
    def init_request(self, environ):
        request = super(ZODBController, self).init_request(environ)
        if self.debug:
            assert self.environ_key == 'schevo.db.zodb' # XXX use settings.SCHEVO['DATABASE_URL']

        if not self.environ_key in request.environ:
            request.environ[self.environ_key] = self.db
        self._request = request # cheat!!!
        return request
