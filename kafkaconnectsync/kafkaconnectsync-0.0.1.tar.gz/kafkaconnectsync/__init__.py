from kafkaconnectsync.utils import isjsonequal, wait_for_client_info
from kafkaconnectsync.client import ConnectClient

"""
Synchronize provided connectors with Kafka Connect sinks.

- If the connector is not present on the API, it will be created.
- If the connector is present on the API:
  - Present on the provided connnectors: it will be updated with the new config (if different)
  - Not present on the provided connectors (and strict=True): delete it
"""
def sync(url, connectors=[], strict=True, wait_for_deployment=True, verbose=False):
  if not url:
    raise RuntimeError('[-] Missing required parameter: "url"')
  
  if connectors == None or len(connectors) == 0:
    if verbose:
      print('[*] No connectors to sync. Exiting...')
    return

  client = ConnectClient(url, verbose)
  if wait_for_deployment:
    # Do not start synchronizing until the API is deployed
    wait_for_client_info(client)

  # Get all connectors from the API
  existing_connectors_ids = client.get_all()
  connectors_ids = map(lambda x: x['config']['name'], connectors)

  # Create or update connectors from object
  for connector in connectors:
    if connector['config']['name'] in existing_connectors_ids:
      # It exists, must update
      current = client.get(connector['config']['name'])
      is_config_equal = isjsonequal(current['config'], connector['config'])
      if not is_config_equal:
        client.update(connector)
    else:
      # Not present, create
      client.create(connector)

  if strict:
    # Delete connector not present on the object anymore
    for connector_id in existing_connectors_ids:
      if not connector_id in connectors_ids:
        # Delete
        client.delete(connector_id)
