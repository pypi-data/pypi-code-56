from shuttle_bus.core.configuration.receive_endpoint_configuration import (
    IReceiveEndpointConfiguration,
)
from shuttle_bus.core.messaging import ReceiveMessageCallBack
from transports.rabbitmq.setting.receive_settings import RabbitMqReceiveSettings


class RabbitMqReceiveEndpointConfigurator(IReceiveEndpointConfiguration):
    def __init__(self):
        self.handler: ReceiveMessageCallBack = None
        self._settings: RabbitMqReceiveSettings = None

    def configure(self, settings: RabbitMqReceiveSettings):
        self._settings = settings

    def apply(self):
        pass

    def set_receive_handler(self, callback: ReceiveMessageCallBack):
        self.handler = callback

    @property
    def handler(self) -> ReceiveMessageCallBack:
        return self.__handler

    @handler.setter
    def handler(self, value: ReceiveMessageCallBack):
        self.__handler = value
