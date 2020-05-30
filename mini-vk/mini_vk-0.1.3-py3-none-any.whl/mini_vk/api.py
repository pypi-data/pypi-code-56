from urllib.parse import urlencode

import requests

VK_API_URL = 'https://api.vk.com/method/'
API_VERSION = '5.102'


class Params:
    def __init__(self, params):
        self.params = params

    def update(self, value):
        self.params.update(value)
        return self.params


class Method:
    def __init__(self, session, url, method, params):
        self.session = session
        self.url = url
        self.method = method
        self.params = params

    def __getattr__(self, item):
        return lambda **params: self.session.get(
            f'{self.url}{self.method}.{item}?{urlencode(self.params.update(params))}'
        )


class API:
    def __init__(self, url, v, token, session):
        self.url = url
        self.token = token
        self.v = v
        self.session = session
        self.params = Params({
            'v': v,
            'access_token': token
        })

    def __getattr__(self, item):
        if item == 'execute':
            return lambda **params: self.session.get(
                f'{self.url}execute?{urlencode(self.params.update(params))}'
            )
        else:
            method = Method(self.session, self.url, item, self.params)
            return method


get_api = lambda token, api_version=API_VERSION, session=requests.Session(): API(VK_API_URL, api_version, token,
                                                                                 session)
