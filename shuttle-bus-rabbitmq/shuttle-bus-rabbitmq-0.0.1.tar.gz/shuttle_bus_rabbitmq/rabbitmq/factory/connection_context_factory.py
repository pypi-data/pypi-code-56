from shuttle_bus.core.transport.settings.host import HostSettings

from shuttle_bus.core.factory import ConnectionContextFactory
from transports.rabbitmq import RabbitMqConnectionContext
from transports.rabbitmq import RabbitMqConnectionContextConfigurator
from transports.rabbitmq import RabbitMqConnectionFactory


class RabbitMqConnectionContextFactory(ConnectionContextFactory):
    @staticmethod
    async def create(
        host_settings: HostSettings,
        configurator=RabbitMqConnectionContextConfigurator(),
    ):
        connection = await RabbitMqConnectionFactory.create(host_settings)

        connection_context = RabbitMqConnectionContext(connection)
        await connection_context.create_channel()

        configurator.apply(connection_context)

        return connection_context
