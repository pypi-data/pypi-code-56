import logging
import json
import requests
import os
import sys


class Report:
    def __init__(self, loglevel):
        self.loglevel = loglevel

        # GET env variables.
        self.KH_REPORTING_URL = os.getenv('KH_REPORTING_URL')

        logging.basicConfig(format='%(asctime)s: %(levelname)s: %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=self.loglevel )

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
            logging.debug("Sending data: "+data) 
            r = requests.post(url = self.KH_REPORTING_URL, json=data)
            r.raise_for_status
        except requests.exceptions.HTTPError as err:
            raise SystemError(err)

    def success(self):
        logging.debug("Check passed")
        data = {"OK": True}
        logging.debug("Sending Data: Ok")
        try:
            self.postResults(data)
        except:
            raise SystemError("Unable to post Resulst")

    def fail(self, message):
        logging.debug("Check failed")
        self.message = message
        data = {"Errors": [message],"OK": False}
        logging.debug("Sending error data: "+  message)
        try: 
            self.postResults(data)
        except:
            raise SystemError("Unable to post Resulst")

