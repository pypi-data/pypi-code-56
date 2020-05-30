from rs4 import asyncore
import re
import time
import sys
import threading
from ..client import baseconnect

DEBUG = False

class OperationalError (Exception): pass
class SQLError (Exception): pass

class ConnectProxy (baseconnect.ConnectProxy):
    def execute_late (self):
        if self._canceled (): # MUST BE CALLED for deactivating asyncon
            return
        request, rs, handle_request_failed = self._args
        self._asyncon.set_timeout (self._timeout)
        try:
            self._asyncon.execute (request)
        except:
            handle_request_failed (rs, self._asyncon)
        self._args = None


class DBConnect (baseconnect.BaseConnect):
    def __init__ (self, address, params = None, lock = None, logger = None):
        super ().__init__ (lock, logger)
        self.address = address
        self.params = params

        # need if there's not any request yet
        self.execute_count = 0
        self.request = None
        self.has_result = False

        self.set_auth ()
        self.set_event_time ()

    def set_auth (self):
        self.dbname, self.user, self.password = "", "", ""
        if not self.params:
            return
        self.dbname, auth = self.params
        if not auth:
            return
        if type (auth) is not tuple:
            self.user = auth
        else:
            try: self.user, self.password = auth
            except ValueError: self.username = auth

    def close_if_over_keep_live (self):
        if self.connected and time.time () - self.event_time > self.keep_alive:
            self.disconnect ()

    def duplicate (self):
        new_asyncon = self.__class__ (self.address, self.params, self.lock, self.logger)
        new_asyncon.keep_alive = self.keep_alive
        new_asyncon.backend = self.backend
        return new_asyncon

    def get_proto (self):
        # call by culster_manager
        return None

    def handle_abort (self):
        # call by dist_call
        self.close ()

    def close (self, deactive = 1):
        addr = type (self.address) is tuple and ("%s:%d" % self.address) or str (self.address)
        if deactive:
            self.logger ("[info] ..dbo %s has been closed" % addr)
            self.set_active (False)
            self.request = None

    def clean_shutdown_control (self, phase, time_in_this_phase):
        self._no_more_request = True
        if self.isactive ():
            return 1
        else:
            self.close ()
            self._no_more_request = False
            return 0

    def maintern (self, object_timeout):
        # when in map, mainteren by lifetime with zombie_timeout
        if self.is_channel_in_map ():
            return False
        idle = time.time () - self.event_time
        if idle > object_timeout:
            self.close (1)
            return True # deletable
        return False

    def reconnect (self):
        self.disconnect ()
        self.connect ()

    def disconnect (self):
        # keep request, just close temporary
        self.close (deactive = 0)

    def close_case (self):
        raise NotImplementedError

    def isconnected (self):
        # self.connected should be defined at __init__ or asyncore
        return self.connected

    def get_execute_count (self):
        return self.execute_count

    def connect (self, force = 0):
        raise NotImplementedError("must be implemented in subclass")

    def handle_timeout (self):
        self.handle_close (OperationalError ("Operation Timeout"))

    def handle_error (self):
        dummy, t, v, info = asyncore.compact_traceback ()
        self.has_result = False
        self.logger.trace ()
        self.handle_close (v)

    def handle_close (self, expt = None):
        if self.expt is None:
            self.expt = expt
        self.close_case_with_end_tran ()
        self.close ()

    def close_case_with_end_tran (self):
        self.end_tran ()
        self.close_case ()

    #-----------------------------------------------------
    # DB methods
    #-----------------------------------------------------
    def fetchall (self):
        raise NotImplementedError

    def end_tran (self):
        raise NotImplementedError

    def begin_tran (self, request):
        if self._no_more_request:
            raise OperationalError ("Entered Shutdown Process")
        self.request = request
        self._history = []
        self.out_buffer = ''
        self.has_result = False
        self.expt = None
        self.execute_count += 1
        self.close_if_over_keep_live ()
        self.set_event_time ()

    def execute (self, request, *args, **kargs):
        self.begin_tran (request)
        raise NotImplementedError("must be implemented in subclass")


class AsynDBConnect (DBConnect):
    def is_channel_in_map (self, map = None):
        if map is None:
            map = self._map
        return self._fileno in map

    def del_channel (self, map=None):
        # do not remove self._fileno
        fd = self._fileno
        if map is None:
            map = self._map
        if fd in map:
            del map[fd]

