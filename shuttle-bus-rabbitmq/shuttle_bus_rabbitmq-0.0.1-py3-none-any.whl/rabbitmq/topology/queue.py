from shuttle_bus.topology.queue.queue import IQueue
from shuttle_bus.topology.setting.exchange import IExchangeSettings
from shuttle_bus.topology.setting.queue import IQueueSettings


class RabbitMqQueueSettings(IExchangeSettings, IQueueSettings, IQueue):
    def __init__(self, queue_name, exchange_type, durable, auto_delete):
        self._exclusive = False

        self._queue_name = queue_name
        self._queue_expiration = None

        super().__init__(queue_name, exchange_type, durable, auto_delete)

    @property
    def exclusive(self):
        return self._exclusive

    def set_queue_argument(self, key, value):
        pass

    @property
    def queue_name(self):
        return self._queue_name

    @property
    def queue_arguments(self):
        return None

    @property
    def queue_expiration(self):
        return self._queue_expiration

    @queue_expiration.setter
    def queue_expiration(self, value):
        self._queue_expiration = value
