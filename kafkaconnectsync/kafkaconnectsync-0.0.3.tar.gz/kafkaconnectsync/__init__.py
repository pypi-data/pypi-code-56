""" main module """
from kafkaconnectsync.utils import isjsonequal, wait_for_client_info
from kafkaconnectsync.client import ConnectClient


def sync(url, connectors, strict=True, wait_for_deployment=True, verbose=False):
    """
    Synchronize provided connectors with Kafka Connect sinks.

    - If the connector is not present on the API, it will be created.
    - If the connector is already present on the API:
    - If it's also present on the local list, the connector will be updated.
    - If strict=True and the connector isn't found on the local list, it'll be deleted from the API.
        If strict=False, the connector will remain as it is.
    """
    if url is None:
        raise RuntimeError('[-] Missing required parameter: "url"')

    if not connectors:
        if verbose:
            print('[*] No connectors to sync. Exiting...')
        return

    client = ConnectClient(url, verbose)
    if wait_for_deployment:
        # Do not start synchronizing until the API is deployed
        wait_for_client_info(client)

    # Get all connectors from the API
    existing_connectors_ids = client.get_all()
    connectors_ids = [conn['config']['name'] for conn in connectors]

    # Create or update connectors from object
    for connector in connectors:
        if connector['config']['name'] in existing_connectors_ids:
            # It exists, must update
            current = client.get(connector['config']['name'])
            is_config_equal = isjsonequal(
                current['config'], connector['config'])
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
