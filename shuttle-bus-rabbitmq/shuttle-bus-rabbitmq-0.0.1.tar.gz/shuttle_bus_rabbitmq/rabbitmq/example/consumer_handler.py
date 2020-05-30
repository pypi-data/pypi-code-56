import aio_pika


class ConsumerHandler:
    def __init__(self):
        self.message = None

    async def consumer_callback(self, message: aio_pika.IncomingMessage):
        async with message.process():
            print("received:", message.body)
            self.message = message.body
