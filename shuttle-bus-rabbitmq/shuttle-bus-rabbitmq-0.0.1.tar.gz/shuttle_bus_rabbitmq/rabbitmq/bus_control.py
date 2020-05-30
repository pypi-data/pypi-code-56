from aio_pika import Queue, Exchange

from shuttle_bus.core.bus_control import BusControl
from transports.rabbitmq import RabbitMqBusFactoryConfigurator
from transports.rabbitmq import RabbitMqConnectionContext
from transports.rabbitmq import RabbitMqContext
from transports.rabbitmq import RabbitMqContextFactory


class RabbitMqBusControl(BusControl):
    def __init__(
        self,
        connection_context: RabbitMqConnectionContext,
        bus_factory_configurator: RabbitMqBusFactoryConfigurator,
    ):
        self._connection_context: RabbitMqConnectionContext = connection_context

        # todo is this the wrong abstraction?
        self._bus_factory_configurator: RabbitMqBusFactoryConfigurator = bus_factory_configurator

        self._context: RabbitMqContext = None
        self._queue: Queue = None
        self._exchange: Exchange = None

    async def start(self):
        queue_name = self.bus_configuration.queue_name
        auto_delete = self.bus_configuration.auto_delete

        connection_context = self._connection_context

        # create bus context
        self._context = await RabbitMqContextFactory.create_context(connection_context)

        # declare queue
        self._queue = await self._context.declare_queue(
            queue_name, auto_delete=auto_delete
        )

        # declare exchange
        self._exchange = await self._context.declare_exchange(
            queue_name,
            auto_delete=auto_delete,
            exchange_type=self.bus_configuration.receive_endpoint_settings.exchange_type,
        )

        # bind
        await self._context.bind_queue_to_exchange(queue_name, queue_name)

        consumer_handler = self.bus_configuration.receive_endpoint_configurator.handler

        await self._context.basic_consumer(queue_name, consumer_handler)

    async def stop(self):
        await self._connection_context.close_connection()

    async def publish(self, message):
        await self._context.basic_publish(self._exchange, message)

    @property
    def connection_context(self):
        return self._connection_context

    @property
    def bus_configuration(self):
        return self._bus_factory_configurator

    @property
    def context(self):
        return self._queue

    @property
    def queue(self):
        return self._queue

    @property
    def exchange(self):
        return self._exchange
