""" ConnectClient class """
import requests


class ConnectClient():
    """
    REST Client for KafkaConnect API
    Implement CRUD operations for kafka connectors
    """

    def __init__(self, url, verbose=False):
        if url is None:
            raise RuntimeError('[-] Missing required parameter: "url"')
        self.url = url
        self.base_endpoint = '{}/connectors'.format(url)
        self.verbose = verbose

    def get_cluster_info(self):
        """ Get cluster information from API entrypoint"""
        response = requests.get(self.url)
        response.raise_for_status()
        return response.json()

    def get_all(self):
        """ Get all connectors """
        response = requests.get(self.base_endpoint)
        response.raise_for_status()
        return response.json()

    def get(self, connector_id):
        """ Get a connector by ID (name) """
        response = requests.get(
            '{}/{}'.format(self.base_endpoint, connector_id))
        response.raise_for_status()
        return response.json()

    def delete(self, connector_id):
        """ Delete a connector by ID """
        response = requests.delete(
            '{}/{}'.format(self.base_endpoint, connector_id))
        response.raise_for_status()
        if self.verbose:
            print('[-] Deleted connector: "{}"'.format(connector_id))

    def create(self, connector):
        """ Create a connector """
        response = requests.post(self.base_endpoint, json={
            'config': connector['config'], 'name': connector['config']['name']})
        response.raise_for_status()
        if self.verbose:
            print('[-] Created connector: "{}"'.format(connector['config']['name']))

    def update(self, connector):
        """ Update a connector config """
        response = requests.put('{}/{}/config'.format(self.base_endpoint,
                                                      connector['config']['name']), json=connector['config'])
        response.raise_for_status()
        if self.verbose:
            print('[-] Updated connector: "{}"'.format(connector['config']['name']))
