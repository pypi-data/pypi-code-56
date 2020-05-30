from shuttle_bus.core.configurator import HostConfigurator
from transports.rabbitmq import RabbitMqHostSettings


class RabbitMqHostConfigurator(HostConfigurator):
    def __init__(self, host, virtual_host):
        self._settings = RabbitMqHostSettings()

        self._settings._host = host
        self._settings._virtual_host = virtual_host

    @property
    def settings(self):
        return self._settings
