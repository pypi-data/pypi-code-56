from urllib.parse import ParseResult, urlparse

from shuttle_bus.core.transport.settings.host import HostSettings


class RabbitMqHostSettings(HostSettings):
    def __init__(self):
        self._host = None
        self._port = None
        self._username = None
        self._password = None
        self._virtual_host = "/"

    @staticmethod
    def create_host_settings(uri):
        settings = RabbitMqHostSettings()
        address: ParseResult = settings._get_host_address(uri)

        settings._host = address.hostname
        settings._port = address.port
        settings._username = address.username
        settings._password = address.password

        return settings

    def _get_host_address(self, address) -> ParseResult:
        parsed_uri = urlparse(address)

        return parsed_uri

    def _is_valid_rabbitmq_scheme(self, scheme) -> bool:
        if scheme is "amqp" or "amqps" or "rabbitmq" or "rabbitmqs":
            return True

        return False

    @property
    def port(self) -> int:
        return self._port

    @property
    def virtual_host(self) -> str:
        return self._virtual_host

    @property
    def username(self) -> str:
        return self._username

    @property
    def password(self) -> str:
        return self._password

    @property
    def host_address(self) -> str:
        return self._host_address

    @property
    def connection_name(self) -> str:
        return self._connection_name

    @property
    def host(self) -> str:
        return self._host
