import logging
import json
import requests
import os
import sys


class Report:
    def __init__(self, **kwargs):
        self.loglevel = kwargs.get('loglevel')

        # GET env variables.
        self.KH_REPORTING_URL = os.getenv('KH_REPORTING_URL')
        if self.loglevel == None:
            level = logging.getLevelName('WARNING')
        else:
            level = logging.getLevelName(self.loglevel)

        logging.basicConfig(format='%(asctime)s: %(levelname)s: %(message)s', level=level)

        logging.warning('Warning logging enabled')
        logging.info('Info logging enabled')
        logging.debug('Debug logging enabled')
        if self.KH_REPORTING_URL == None:
            logging.error('KH_REPORTING_URL not found.  Cannot procceed')
            sys.exit()
        else:
            logging.info('Kuberhealhty Reportin URL: ' + self.KH_REPORTING_URL)

    def postResults(self, data):
        # Send Request:
        try:
            logging.debug("Sending data: "+str(data)) 
            r = requests.post(url = self.KH_REPORTING_URL, json=data)
            r.raise_for_status
        except requests.exceptions.HTTPError as err:
            raise SystemError(err)

    def success(self):
        logging.debug("Check passed")
        data = {"OK": True}
        logging.debug("Sending Data: " + str(data))
        try:
            self.postResults(data)
        except:
            raise SystemError("Unable to post Resulst")

    def fail(self, message):
        logging.debug("Check failed")
        self.message = message
        data = {"Errors": [str(message)],"OK": False}
        logging.debug("Sending error data: "+  str(message))
        try: 
            self.postResults(data)
        except:
            raise SystemError("Unable to post Resulst")

