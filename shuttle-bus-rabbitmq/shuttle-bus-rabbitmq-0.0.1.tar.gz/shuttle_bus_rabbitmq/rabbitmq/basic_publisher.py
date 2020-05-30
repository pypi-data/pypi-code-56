from aio_pika import Message, Exchange

from shuttle_bus.core.publisher import IPublisher


class BasicPublisher(IPublisher):
    async def publish(self, exchange: Exchange, routing_key, body, headers=None):
        message = Message(body=body, content_type="text/plain", headers=headers)

        await exchange.publish(message, routing_key)
