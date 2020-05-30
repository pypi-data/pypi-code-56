from shuttle_bus.topology.setting.queue import IQueueSettings
from shuttle_bus.topology.setting.queue_binding import IQueueBindingSettings


class RabbitMqQueueBindingSettings(IQueueSettings, IQueueBindingSettings):
    def __init__(self, queue_name, exchange_type, durable, auto_delete):
        self._routing_key = ""

        super().__init__(queue_name, exchange_type, durable, auto_delete)

    @property
    def routing_key(self):
        return self._routing_key

    @routing_key.setter
    def routing_key(self, value):
        self._routing_key = value

    def set_binding_argument(self, key, value):
        pass
