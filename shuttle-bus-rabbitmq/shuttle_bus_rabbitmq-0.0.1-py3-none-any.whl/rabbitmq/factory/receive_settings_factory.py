from shuttle_bus.core.factory import ReceiveSettingsFactory
from transports.rabbitmq import RabbitMqReceiveSettings


class RabbitMqReceiveSettingsFactory(ReceiveSettingsFactory):
    @staticmethod
    def get_receive_settings(queue_name, auto_delete=False) -> RabbitMqReceiveSettings:
        receive_settings = RabbitMqReceiveSettings(queue_name)
        receive_settings.auto_delete = auto_delete

        return receive_settings
