__version__ = '0.1.1'

from aircloak_tools import aircloak_client
from contextlib import contextmanager


@contextmanager
def connect(host, port, user, password, dataset):
    try:
        ac = aircloak_client.AircloakConnection(
            host=host, port=port, user=user, password=password, dataset=dataset)
        yield ac
    finally:
        ac.close()
