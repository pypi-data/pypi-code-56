import requests

"""
REST Client for KafkaConnect API
Implement CRUD operations for kafka connectors
"""
class ConnectClient:
  def __init__(self, url, verbose=False):
    if not url:
      raise RuntimeError('[-] Missing required parameter: "url"')
    self.url = url
    self.base_endpoint = '{}/connectors'.format(url)
    self.verbose = verbose

  """ Get cluster information from API entrypoint"""
  def get_cluster_info(self):
    response = requests.get(self.url)
    response.raise_for_status()
    return response.json()

  """ Get all connectors """
  def get_all(self):
    response = requests.get(self.base_endpoint)
    response.raise_for_status()
    return response.json()

  """ Get a connector by ID (name) """
  def get(self, connector_id):
    response = requests.get('{}/{}'.format(self.base_endpoint, connector_id))
    response.raise_for_status()
    return response.json()

  """ Delete a connector by ID """
  def delete(self, connector_id):
    response = requests.delete('{}/{}'.format(self.base_endpoint, connector_id))
    response.raise_for_status()
    if self.verbose:
      print('[-] Deleted connector: "{}"'.format(connector_id))

  """ Create a connector """
  def create(self, connector):
    response = requests.post(self.base_endpoint, json={ 'config': connector['config'], 'name': connector['config']['name'] })
    response.raise_for_status()
    if self.verbose:
      print('[-] Created connector: "{}"'.format(connector['config']['name']))

  """ Update a connector config """
  def update(self, connector):
    response = requests.put('{}/{}/config'.format(self.base_endpoint, connector['config']['name']), json=connector['config'])
    response.raise_for_status()
    if self.verbose:
      print('[-] Updated connector: "{}"'.format(connector['config']['name']))
