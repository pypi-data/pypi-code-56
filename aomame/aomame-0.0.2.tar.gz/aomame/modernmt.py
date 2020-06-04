
import requests

from aomame.exceptions import ResponseError

class ModernmtTranslator:
    def __init__(self, host, key):
        # Default host: api.modernmt.eu/
        self.host, self.key = host, key
        self.headers = {'MMT-ApiKey': self.key}

        # See https://www.modernmt.com/api/
        self.endpoints = {'translate': 'translate',
                          'context-vector': 'context-vector',
                          'languages': 'languages'}

        self.urls = {k:"https://" + self.host + '/' + v for k,v in self.endpoints.items()}

    def api_call(self, operation, method, params=None, json=None):
        return operation(self.urls[method], params=params)

    def languages(self):
        response = self.api_call(requests.get, 'languages')
        return set(response.json()['data'].keys())

    def translate(self, text, srclang, trglang):
        params = (('source', srclang), ('target', trglang), ('q', text.strip()),)
        response = self.api_call(requests.get, 'translate', params=params)
        return response
