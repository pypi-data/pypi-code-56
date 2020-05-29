import time
from pathlib import Path

import fire
import toml
from termcolor import colored, cprint

from datactl.data_config import Config
from datactl.mongodb import MongoDB
from datactl.rabbitmq import RabbitMQ
from datactl.celery import Celery
from datactl.redis import Redis
from datactl.utils import abort, get_value, prepare_data, require_file, show_data, to_list_of_dict

CONFIG_PATH = require_file(Path.home() / '.datactl' / 'config.toml')
config = toml.load(CONFIG_PATH)


class Generator():

    def __init__(self,
                 uri=None,
                 queue=None,
                 collection=None,
                 database=None,
                 size=None,
                 metadata=None,
                 template=None,
                 template_file=None,
                 from_config=None,
                 yes=None,
                 limit=None,
                 offset=None,
                 output=None,
                 dry_run=None,
                 table=None,
                 columns=None,
                 hide=None,
                 timeout=None,
                 exchange=None,
                 routing_key=None,
                 broker=None,
                 backend=None,
                 endpoint=None,
                 exchange_type=None,
                 data=None,
                 ):
        if template_file and not Path(template_file).exists():
            cprint(colored('file [%s] does not exists' %
                           template_file, color='red'))
            abort()
        config_obj = Config(self)
        self._uri = get_value(
            uri, 'uri', from_config=from_config, config_obj=config_obj, )
        self._queue = get_value(
            queue, 'queue', from_config=from_config, config_obj=config_obj, )
        self._collection = get_value(
            collection, 'collection', from_config=from_config, config_obj=config_obj, )
        self._database = get_value(
            database, 'database', from_config=from_config, config_obj=config_obj, )
        self._size = get_value(size, 'size', from_config=from_config,
                               config_obj=config_obj, ttype=int, default=1)
        self._metadata = get_value(
            metadata, 'metadata', from_config=from_config, config_obj=config_obj, ttype=bool, default=False)
        self._template = get_value(
            template, 'template', from_config=from_config, config_obj=config_obj)
        self._template_file = get_value(
            template_file, 'template_file', from_config=from_config, config_obj=config_obj)
        self._from_config = get_value(
            from_config, 'from_config', from_config=from_config, config_obj=config_obj)
        self._yes = get_value(yes, 'yes', from_config=from_config,
                              config_obj=config_obj, ttype=bool, default=False)
        self._limit = get_value(limit, 'limit', from_config=from_config,
                                config_obj=config_obj, ttype=int, default=50)
        self._offset = get_value(
            offset, 'offset', from_config=from_config, config_obj=config_obj, ttype=int, default=0)
        self._output = get_value(output, 'output', from_config=from_config,
                                 config_obj=config_obj, ttype=str, default='table')
        self._dry_run = get_value(dry_run, 'dry_run', from_config=from_config,
                                  config_obj=config_obj, ttype=bool, default=False)
        self._table = get_value(
            table, 'table', from_config=from_config, config_obj=config_obj,)
        self._columns = get_value(
            columns, 'columns', from_config=from_config, config_obj=config_obj,)
        self._hide = get_value(
            hide, 'hide', from_config=from_config, config_obj=config_obj,)
        self._timeout = get_value(
            timeout, 'timeout', from_config=from_config, config_obj=config_obj, ttype=int, default=6)
        self._exchange = get_value(
            exchange, 'exchange', from_config=from_config, config_obj=config_obj, ttype=str, default='')
        self._routing_key = get_value(
            routing_key, 'routing_key', from_config=from_config, config_obj=config_obj, ttype=str, default='')
        self._broker = get_value(
            broker, 'broker', from_config=from_config, config_obj=config_obj)
        self._backend = get_value(
            backend, 'backend', from_config=from_config, config_obj=config_obj)
        self._endpoint = get_value(
            endpoint, 'endpoint', from_config=from_config, config_obj=config_obj)
        self._exchange_type = get_value(
            exchange_type, 'exchange_type', from_config=from_config, config_obj=config_obj)
        self._data = get_value(data, 'data', from_config=from_config, config_obj=config_obj)
        self._config = config_obj
        self.config = Config(self)
        self.rabbitmq = RabbitMQ(self)
        self.redis = Redis(self)
        self.mongodb = MongoDB(self)
        self.celery = Celery(self)
        self.generate = self._generate

    def _generate(self, msg='', size=None):
        '''
        generate some data
        '''
        self._size = abs(size if size is not None else self._size)
        data = prepare_data(str(msg), self)
        data = to_list_of_dict(data)
        show_data(data, self)


def main():
    start_time = time.time()
    fire.Fire(Generator)
    elapsed_time = time.time() - start_time
    cprint(colored('elapsed time: %s seconds' % elapsed_time, color='yellow'))
