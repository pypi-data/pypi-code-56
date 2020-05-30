from aio_pika import exceptions, Exchange
from aio_pika.channel import Channel
from aio_pika.connection import Connection
from aio_pika.queue import Queue

from shuttle_bus.core.context import ModelContext
from shuttle_bus.core.exceptions.queue_precondition import QueuePreconditionFailed
from transports.rabbitmq.basic_publisher import BasicPublisher


class RabbitMqContext(ModelContext):
    def __init__(self, connection_context):
        self._connection_context = connection_context
        self._connection: Connection = connection_context.connection
        self._channel: Channel = connection_context.channel

        self._publisher = BasicPublisher()

    async def dispose(self):
        await self._connection_context.close_connection()

    async def declare_queue(
        self, queue_name, auto_delete: bool = False, arguments=None
    ) -> Queue:

        try:
            return await self._channel.declare_queue(
                queue_name, auto_delete=auto_delete, arguments=arguments
            )
        except exceptions.ChannelPreconditionFailed as precondition_failed:
            raise QueuePreconditionFailed(
                "declare_queue exception", precondition_failed
            )

    async def recreate_queue(
        self, queue_name, auto_delete: bool = False, arguments=None
    ) -> Queue:
        delete_ok = await self.delete_queue(queue_name)
        if delete_ok:
            return await self.declare_queue(
                queue_name, auto_delete=auto_delete, arguments=arguments
            )
        raise Exception("recreate_queue error: could delete queue")

    async def declare_exchange(
        self, exchange_name, auto_delete: bool = False, exchange_type="direct"
    ) -> Exchange:
        return await self._channel.declare_exchange(
            exchange_name, auto_delete=auto_delete, type=exchange_type
        )

    async def delete_exchange(self, exchange_name):
        return await self._channel.exchange_delete(exchange_name)

    async def purge_queue(self, queue_name):
        queue: Queue = await self.get_queue(queue_name)
        await queue.purge()

    async def get_queue(self, queue_name) -> Queue:
        try:
            return await self._channel.get_queue(queue_name)
        except exceptions.ChannelClosed:
            return None

    async def get_exchange(self, exchange_name) -> Exchange:
        try:
            return await self._channel.get_exchange(exchange_name)
        except exceptions.ChannelClosed:
            return None

    async def delete_queue(self, queue_name):
        return await self._channel.queue_delete(queue_name)

    async def basic_consumer(self, consumer, consumer_callback):
        consumer_queue: Queue = await self.get_queue(consumer)
        consumer_tag = await consumer_queue.consume(callback=consumer_callback)

        return consumer_tag

    async def basic_publish(self, exchange, body, routing_key=""):
        await self._publisher.publish(
            exchange=exchange, routing_key=routing_key, body=body
        )

    async def bind_queue_to_exchange(self, queue_name, exchange_name, routing_key=""):
        await self._channel.channel.queue_bind(
            queue=queue_name, exchange=exchange_name, routing_key=routing_key
        )

    async def bind_exchange_to_exchange(
        self, bind_exchange_name, to_exchange_name, routing_key
    ):
        await self._channel.channel.exchange_bind(
            destination=to_exchange_name,
            source=bind_exchange_name,
            routing_key=routing_key,
        )
