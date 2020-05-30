from shuttle_bus.topology.exchange.exchange import IExchange
from shuttle_bus.topology.setting.exchange import IExchangeSettings


class RabbitMqExchangeSettings(IExchangeSettings, IExchange):
    def __init__(self, exchange_name, exchange_type, durable=False, auto_delete=False):
        self.auto_delete = auto_delete
        self._exchange_name = exchange_name
        self._exchange_type = exchange_type
        self._durable = durable

    def set_exchange_argument(self, key, value):
        pass

    @property
    def exchange_name(self):
        return self._exchange_name

    @property
    def exchange_type(self):
        return self._exchange_type

    @property
    def durable(self):
        return self._durable

    @property
    def auto_delete(self):
        return self.__auto_delete

    @auto_delete.setter
    def auto_delete(self, value):
        self.__auto_delete = value
