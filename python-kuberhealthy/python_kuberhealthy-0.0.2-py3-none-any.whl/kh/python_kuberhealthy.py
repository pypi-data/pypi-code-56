import logging
import json
import requests
import os


class Report:
    def __init__(self, loglevel):
        self.loglevel = loglevel

        # GET env variables.
        self.KH_REPORTING_URL = os.getenv('KH_REPORTING_URL')

        logging.basicConfig(format='%(asctime)s: %(levelname)s: %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=self.loglevel )

        logging.warning('Warning logging enabled')
        logging.info('Info logging enabled')
        logging.debug('Debug logging enabled')
        logging.info('Kuberhealhty Reportin URL: ' + self.KH_REPORTING_URL)

    def postResults(self, data):
        # Send Request:
        try: 
            r = requests.post(url = self.KH_REPORTING_URL, json=data)
            r.raise_for_status
        except requests.exceptions.HTTPError as err:
            raise SystemError(err)

    def sendOK(self):
        data = {"OK": True}
        logging.debug("Sending Data: Ok")
        self.postResults(data)

    def sendError(self, message):
        self.message = message
        data = {"Errors": [message],"OK": False}
        logging.debug("Sending Data: "+  message)
        self.postResults(data)
