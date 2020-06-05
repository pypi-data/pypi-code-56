from .event_broker import EventBroker
from .platform_mock_api import PlatformMockApi


class PlatformMockApiFactory:
    @classmethod
    def mqtt(cls, mqtt_address: str,
             mqtt_username: str,
             mqtt_password: str,
             sender_name: str,
             event_handler) -> PlatformMockApi:
        import uuid
        client_id = sender_name + ":" + str(uuid.uuid4())
        event_broker = EventBroker(
            mqtt_address=mqtt_address,
            mqtt_username=mqtt_username,
            mqtt_password=mqtt_password,
            client_id=client_id,
            event_handler=event_handler
        )
        platform_mock_api = PlatformMockApi(event_broker, sender_name)
        return platform_mock_api
