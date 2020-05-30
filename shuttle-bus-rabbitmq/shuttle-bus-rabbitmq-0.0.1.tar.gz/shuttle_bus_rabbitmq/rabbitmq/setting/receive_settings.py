from shuttle_bus.core.transport.settings.receive_settings import ReceiveSettings

from transports.rabbitmq.topology.queue_binding import QueueBindingSettings


class RabbitMqReceiveSettings(QueueBindingSettings, ReceiveSettings):
    @property
    def prefetch_count(self):
        return self._prefetch_count

    @property
    def exclusive(self):
        return self._exclusive

    @property
    def bind_queue(self) -> bool:
        return self._bind_queue

    @property
    def no_ack(self) -> bool:
        return self._no_ack

    def __init__(self, name, durable=False, auto_delete=False, exchange_type="fanout"):
        self._prefetch_count = None
        self._exclusive = False
        self._bind_queue = False
        self._no_ack = False

        super().__init__(name, exchange_type, durable, auto_delete)
