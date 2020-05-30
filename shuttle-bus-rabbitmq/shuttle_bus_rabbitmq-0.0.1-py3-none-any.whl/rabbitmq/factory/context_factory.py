from shuttle_bus.core.factory import ModelContextFactory
from transports.rabbitmq import RabbitMqConnectionContext
from transports.rabbitmq import RabbitMqContext


class RabbitMqContextFactory(ModelContextFactory):
    @staticmethod
    async def create_context(
        connection_context: RabbitMqConnectionContext,
    ) -> RabbitMqContext:
        context = RabbitMqContext(connection_context=connection_context)

        return context
