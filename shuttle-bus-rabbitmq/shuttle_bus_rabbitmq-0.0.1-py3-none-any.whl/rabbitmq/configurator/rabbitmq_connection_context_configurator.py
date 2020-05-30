from shuttle_bus.core.configurator.conection_context_configurator import (
    ConnectionContextConfigurator,
)
from transports.rabbitmq import RabbitMqConnectionContext


class RabbitMqConnectionContextConfigurator(ConnectionContextConfigurator):
    def __init__(self):
        self._connection_close_callback = None
        self._channel_close_callback = None

    def configure(self, connection_close_callback=None, channel_close_callback=None):
        self._connection_close_callback = connection_close_callback
        self._channel_close_callback = channel_close_callback

    def apply(self, connection_context: RabbitMqConnectionContext):

        if self._connection_close_callback:
            connection_context.add_connection_close_callback(
                self._connection_close_callback
            )

        if self._channel_close_callback:
            connection_context.add_channel_close_callback(self._channel_close_callback)
