import os
import IPython
import logging
import requests

from abc import ABC, abstractmethod
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

DIR = os.path.dirname(os.path.realpath(__file__))

OPERATIONS = {
    x.rsplit('.', 1)[0]: (lambda x: open(x).read())(os.path.join(
        DIR, 'graphql/operations', x))
    for x in os.listdir(os.path.join(DIR, 'graphql/operations'))
    if x.endswith('.gql')
}


class Resource(ABC):
    @abstractmethod
    def execute(self, instruction):
        pass

    @abstractmethod
    def terminate(self):
        pass


class Bot(ABC):
    def __init__(self, endpoint, username, password, resources, waiter):
        self._waiter = waiter
        self.state = {}
        self.terminate = False
        self.logger = logging.getLogger('BOT_{}'.format(
            self.__class__.__name__.upper()))

        for key, value in resources.items():
            setattr(self, key, value)

        login_response = requests.post(
            'https://{}//ibis/login-pass/'.format(endpoint),
            data={
                'username': username,
                'password': password
            })

        self.gid = login_response.json()['user_id']
        if not self.gid:
            pass  # log error and exit

        self._client = Client(
            transport=RequestsHTTPTransport(
                url='https://{}/graphql/'.format(endpoint),
                cookies=login_response.cookies))

    def api_operate_defined(self, name, variables=None):
        operation = gql(OPERATIONS[name])
        self._client.execute(operation, variables=variables)

    def api_operate_custom(self, operation, variables=None):
        self._client.execute(gql(operation), variables=variables)

    def api_wait(self, operation, variables=None):
        self._waiter.wait()

    def save_state(self):
        pass  # save state to SQLite database

    def interact(self):
        IPython.embed()

    # Methods to implement

    @abstractmethod
    def start(self, **kwargs):
        pass

    @abstractmethod
    def run(self):
        pass

    @abstractmethod
    def execute(self, instruction):
        pass
