""" utils """
import time
from requests import exceptions
from jsondiff import diff


def isjsonequal(base, obj):
    """ Compare two json objects and return true if they are deeply equal """
    result = diff(base, obj)
    keys = len(result.keys())
    return keys == 0


def wait_for_client_info(client, timeout=300, debug=False):
    """
    Function to wait until the kafka client is accesible.
    Do not return until it can get the client info.
    """
    start = time.time()
    while time.time() - start < timeout:
        time.sleep(10)
        try:
            response = client.get_cluster_info()
            if response['kafka_cluster_id']:
                return response['kafka_cluster_id']
        except exceptions.RequestException:
            if debug:
                print('[+] Waiting for Kafka Connect to be ready...')

    raise RuntimeError('[-] Kafka Connect client timeout exceeded')
