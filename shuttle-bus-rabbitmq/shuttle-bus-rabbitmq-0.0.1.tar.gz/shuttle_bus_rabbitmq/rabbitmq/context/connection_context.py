from aio_pika import connection as rabbitmq_connection, Connection

from shuttle_bus.core.context import ConnectionContext


class RabbitMqConnectionContext(ConnectionContext):
    def __init__(self, connection: Connection):
        self._connection = connection
        self._channel = None

        self.add_connection_close_callback(self._on_connection_close)

    def add_connection_close_callback(self, close_callback):
        self._connection.add_close_callback(callback=close_callback)

    def add_channel_close_callback(self, close_callback):
        self._channel.add_close_callback(callback=close_callback)

    async def create_channel(self, close_callback=None):
        self._channel = await self._connection.channel()
        self.add_channel_close_callback(self.add_channel_close_callback)

        if close_callback is not None:
            self.add_channel_close_callback(close_callback)

    @property
    def channel(self) -> rabbitmq_connection.Channel:
        return self._channel

    @property
    def connection(self) -> rabbitmq_connection.Connection:
        return self._connection

    def _on_connection_close(self, args):
        print(
            ":: RabbitMqConnectionContext_on_connection_close: closing connection", args
        )
        self._cleanup_connection()

    def _on_channel_close(self, args):
        print(":: RabbitMqConnectionContext_on_channel_close: closing connection", args)

        self._cleanup_connection()

    async def _reopen_closed_connect(self):
        if self._channel.is_closed:
            await self._channel.reopen()

    async def close_connection(self):
        await self._connection.close()

    def _cleanup_connection(self):
        if self._connection is not None and self._connection.is_closed is not True:
            self._connection.close()
