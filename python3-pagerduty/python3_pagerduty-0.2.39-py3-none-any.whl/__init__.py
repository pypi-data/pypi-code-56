#!/usr/bin/env python

try:
    import json
except ImportError:
    import simplejson as json

import requests
import sys
from pagerduty.version import *

__version__ = VERSION

class PagerDutyException(Exception):
    def __init__(self, status, message, errors=None):
        super(PagerDutyException, self).__init__(message)
        self.msg = message
        self.status = status
        self.errors = errors
    
    def __repr__(self):
        return "%s(%r, %r, %r)" % (self.__class__.__name__, self.status, self.msg, self.errors)
    
    def __str__(self):
        txt = "%s: %s" % (self.status, self.msg)
        if self.errors:
            txt += "\n" + "\n".join("* %s" % x for x in self.errors)
        return txt

class PagerDuty(object):
    def __init__(self, service_key, https=True, timeout=15):
        self.service_key = service_key
        self.api_endpoint = ("http", "https")[https] + "://events.pagerduty.com/generic/2010-04-15/create_event.json"
        self.timeout = timeout
    
    def trigger(self, description, incident_key=None, details=None):
        description = bytes(description, 'UTF-8')
        return self._request("trigger", description=description, incident_key=incident_key, details=details)
    
    def acknowledge(self, incident_key, description=None, details=None):
        return self._request("acknowledge", description=description, incident_key=incident_key, details=details)
    
    def resolve(self, incident_key, description=None, details=None):
        return self._request("resolve", description=description, incident_key=incident_key, details=details)
    
    def _request(self, event_type, **kwargs):
        event = {
            "service_key": self.service_key,
            "event_type": event_type,
        }
        for k, v in list(kwargs.items()):
            if v is not None:
                print("Key {0} has value {1}".format(k,v), file=sys.stderr)
                event[k] = v

        print("EVENT: {0}".format(event), file=sys.stderr)
        encoded_event = json.dumps(str(event))
        print("ENCODED_ENVT: {0}".format(encoded_event), file=sys.stderr)
        try:
            res = requests.post(self.api_endpoint, data=encoded_event)
        except Exception as e:
            print("Exception: {0}".format(e), file=sys.stderr)
        result = json.loads(res.text)
        print("STATUS {0}".format(res.status_code), file=sys.stderr)
        if res.status_code != requests.codes.ok:
            raise PagerDutyException(res.status_code, res.text, result['errors'])
        
        # if result['warnings]: ...
        
        return result.get('incident_key')
