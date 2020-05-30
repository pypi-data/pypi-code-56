from shuttle_bus.core.factory import BusControlFactory
from transports.rabbitmq import RabbitMqBusControl
from transports.rabbitmq import RabbitMqBusFactoryConfigurator
from transports.rabbitmq import RabbitMqConnectionContextConfigurator
from transports.rabbitmq import RabbitMqConnectionContextFactory


class RabbitMqBusControlFactory(BusControlFactory):
    @staticmethod
    async def create(
        bus_configurator: RabbitMqBusFactoryConfigurator,
    ) -> RabbitMqBusControl:
        host_settings = bus_configurator.host_settings

        connection_context_configurator = RabbitMqConnectionContextConfigurator()
        connection_context_configurator.configure()

        # todo this creates a connection so maybe it should be created in bus_control.start()
        connection_context = await RabbitMqConnectionContextFactory.create(
            host_settings, connection_context_configurator
        )

        bus_control = RabbitMqBusControl(connection_context, bus_configurator)

        return bus_control


class RabbitMqHostSettingsFactory(HostSettingsFactory):
    @staticmethod
    def get_host_settings(uri) -> RabbitMqHostSettings:
        # todo check uri for queue_name
        host_settings = RabbitMqHostSettings.create_host_settings(uri)

        return host_settings
