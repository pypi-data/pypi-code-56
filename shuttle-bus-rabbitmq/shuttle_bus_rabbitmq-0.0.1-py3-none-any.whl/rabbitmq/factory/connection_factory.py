from aio_pika import connect_robust, exceptions
from shuttle_bus.core.transport.settings.host import HostSettings

from shuttle_bus.core.factory import ConnectionFactory


class RabbitMqConnectionFactory(ConnectionFactory):
    @staticmethod
    async def create(host_settings: HostSettings):

        try:
            connection = await connect_robust(
                host=host_settings.host,
                port=host_settings.port,
                virtualhost=host_settings.virtual_host,
                login=host_settings.username,
                password=host_settings.password,
            )
            return connection

        # todo handle connection exceptions.
        # todo check what mass transit does when no connection to broker?
        except exceptions.AMQPException as protocol_exception:
            print("connect exception", protocol_exception)
        except Exception as exception:
            raise exception
