from transports.rabbitmq import RabbitMqReceiveSettings


class RabbitMqBusConfiguration:
    def __init__(self, host_settings, receive_endpoint_settings):
        self._host_settings = host_settings
        self._receive_endpoint_settings = receive_endpoint_settings

    @property
    def host_settings(self):
        return self._host_settings

    @property
    def receive_endpoint_settings(self) -> RabbitMqReceiveSettings:
        return self._receive_endpoint_settings
