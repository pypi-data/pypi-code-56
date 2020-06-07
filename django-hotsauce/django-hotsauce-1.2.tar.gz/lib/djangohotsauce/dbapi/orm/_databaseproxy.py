#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Copyright (C) 2007-2020 Jack Bortone <jack@isotopesoftware.ca>
# All rights reserved.
"""Schevo database wrappers."""

__all__ = ['ConnectionError', 'DatabaseProxy']

#import schevo.database
from schevo.database import format_dbclass

# mulithreading support
import schevo
import schevo.mt

class ConnectionError(Exception):
    """Error connecting to the selected DB backend"""
    pass

class DatabaseProxy(object):
    """Creates and manages live ``Database`` objects using Proxy
    style attribute delegation.

    Usage::

        >>> from djangohotsauce.dbapi.orm import DatabaseProxy
        >>> db = DatabaseProxy('moviereviews') # access the "moviereviews" database
        >>> article = db.Article.findone(uid=2201)

    """

    db_version = 2
    db_backend = format_dbclass[db_version]
    DatabaseClass = db_backend
    
    def __init__(self, db_host='localhost', db_port=4545, debug_level=0,
        autosync=False):
        self.conn = None
        self.db = None
        self.db_name = "%s:%d" % (db_host, db_port)
        self.db_is_open = False
        if not self.db_is_open:
            self.safe_open_zodb(self.db_name)
    
    def safe_open_zodb(self, db_name, multithread=True):
        self.conn = self.db_backend(db_name)
        if not self.conn._is_open == True:
            self.conn.open()

        #import pdb; pdb.set_trace()
        self.root = self.conn.get_root()
        # perform a quick sanity check
        assert 'SCHEVO' in self.root, 'Not a Schevo database or unexpected DB format: %r' % db_name
        self.db = self.DatabaseClass(self.conn)
        self.db_is_open = True
        if multithread:
            schevo.mt.install(self.db)
        return None

    def __getattr__(self, attr):
        lock = self.db.read_lock()
        with lock:
            try:
                return getattr(self.db, attr)
            except AttributeError:
                raise 
        lock.release()        

    def __repr__(self):
        return str("<Database: version=%d name=%s backend=%s>" % \
            (self.db_version, self.db_name, self.DatabaseClass))

    def commit(self):
        """Invoke underlaying ``commit`` method"""
        self.conn._commit()
        return None
