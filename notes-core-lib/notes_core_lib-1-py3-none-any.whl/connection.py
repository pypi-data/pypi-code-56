from . import config
import psycopg2

class Connection:

    def __init__(self):
        self._path = None
        self._connection = None

    def set_path(self, path):
        self._path = path

    def make_connection(self):
        cfg = config.load(self._path)
        db_config = cfg["database"]
        self._connection = psycopg2.connect(dbname=db_config["database"], host=db_config["host"], user=db_config["user"], password=db_config["password"])
        return self._connection

    def get_connection(self):
        return self._connection

