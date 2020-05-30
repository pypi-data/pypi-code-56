import asyncio

from shuttle_bus.core.factory import RabbitMqHostSettingsFactory
from shuttle_bus.core.factory import RabbitMqReceiveSettingsFactory
from transports.rabbitmq import RabbitMqBusConfiguration
from transports.rabbitmq import RabbitMqBusControlFactory
from transports.rabbitmq import RabbitMqBusFactoryConfigurator
from transports.rabbitmq import RabbitMqReceiveEndpointConfigurator
from transports.rabbitmq import ReceiveMessage


async def consumer_callback(message: ReceiveMessage):
    async with message.process():
        print("received message:", message.body.decode("UTF-8"))


async def do():
    uri = "amqp://admin:admin@127.0.0.1/"
    host_settings = RabbitMqHostSettingsFactory.get_host_settings(uri)

    queue_name = "shuttle_bus_sample_consume_from_queue_another"
    receive_settings = RabbitMqReceiveSettingsFactory.get_receive_settings(
        queue_name, auto_delete=False
    )

    bus_configuration = RabbitMqBusConfiguration(host_settings, receive_settings)
    bus_factory_configurator = RabbitMqBusFactoryConfigurator(bus_configuration)

    # todo queue name formatter
    # todo add queue setting

    receive_endpoint_configurator = RabbitMqReceiveEndpointConfigurator()
    receive_endpoint_configurator.configure(receive_settings)
    receive_endpoint_configurator.set_receive_handler(consumer_callback)

    bus_factory_configurator.receive_endpoint(receive_endpoint_configurator)

    bus = await RabbitMqBusControlFactory.create(bus_factory_configurator)

    await bus.start()
    await bus.publish(bytes("Hello", "utf-8"))
    await bus.stop()


def main():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(do())


if __name__ == "__main__":
    main()
