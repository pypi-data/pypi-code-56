from shuttle_bus.core.transport.settings.host import HostSettings

from shuttle_bus.core.configurator import BusFactoryConfigurator
from transports.rabbitmq import RabbitMqBusConfiguration
from transports.rabbitmq import RabbitMqReceiveEndpointConfigurator
from transports.rabbitmq import RabbitMqReceiveSettings


# todo inherit add receive endpoint configurator
class RabbitMqBusFactoryConfigurator(BusFactoryConfigurator):
    def __init__(self, bus_configuration: RabbitMqBusConfiguration):
        self._host_settings = bus_configuration.host_settings
        self._receive_endpoint_settings = bus_configuration.receive_endpoint_settings

        self._receive_endpoint_configurator: RabbitMqReceiveEndpointConfigurator = None

    @property
    def auto_delete(self):
        return self._receive_endpoint_settings.auto_delete

    @property
    def queue_name(self):
        return self._receive_endpoint_settings.queue_name

    @property
    def receive_endpoint_settings(self) -> RabbitMqReceiveSettings:
        return self._receive_endpoint_settings

    @property
    def host_settings(self) -> HostSettings:
        return self._host_settings

    @property
    def receive_endpoint_configurator(self) -> RabbitMqReceiveEndpointConfigurator:
        return self._receive_endpoint_configurator

    def receive_endpoint(
        self, configurator: RabbitMqReceiveEndpointConfigurator, name_formatter=None
    ):
        self._receive_endpoint_configurator = configurator
