# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['shuttle_bus_rabbitmq',
 'shuttle_bus_rabbitmq.rabbitmq',
 'shuttle_bus_rabbitmq.rabbitmq.configuration',
 'shuttle_bus_rabbitmq.rabbitmq.configurator',
 'shuttle_bus_rabbitmq.rabbitmq.context',
 'shuttle_bus_rabbitmq.rabbitmq.example',
 'shuttle_bus_rabbitmq.rabbitmq.factory',
 'shuttle_bus_rabbitmq.rabbitmq.setting',
 'shuttle_bus_rabbitmq.rabbitmq.topology']

package_data = \
{'': ['*']}

install_requires = \
['aio_pika>=6.6.0,<7.0.0', 'typing_extensions>=3.7.4,<4.0.0']

setup_kwargs = {
    'name': 'shuttle-bus-rabbitmq',
    'version': '0.0.1',
    'description': '',
    'long_description': '# Shuttle Bus\n\nA modern distributed application framework for Python.\n\n## Build Status\n\n| Branch | Status |\n| :--- | :---: |\n| master | [![master](https://github.com/jbw/shuttle-bus/workflows/Python%20package/badge.svg)](./) |\n| develop | [![develop](https://github.com/jbw/shuttle-bus/workflows/Python%20package/badge.svg?branch=develop)](./) |\n\n## Getting started\n\n### Install\n\n```bash\npip install shuttle-bus-rabbitmq\n```\n\n### Simple example\n\n```python\nuri = "amqp://admin:admin@localhost/"\nhost_settings = HostSettings.create(uri)\n\nreceive_settings = ReceiveSettings()\nreceive_settings.name = "queue_name"\n\nconsumer = PrintConsumer()\nreceive_endpoint_configuration = ReceiveEndpointConfiguration(receive_settings, consumer)\n\nbus_configuration = BusConfiguration(host_settings)\n\nbus = await Bus.create(bus_configuration, receive_endpoint_configuration)\n\nawait bus.start()\nawait bus.publish(bytes("Hello", "UTF-8"))\nawait bus.stop()\n```\n\n## Versioning\n\nShuttle Bus follows Semantic Versioning.\n\n## Contributing\n\nSee CONTRIBUTING.md\n\n## Builds\n\nSee [https://pypi.org/project/shuttle-bus/](https://pypi.org/project/shuttle-bus/)\n\n## Requirements\n\n* Python &gt;= 3.6\n\n## Credits\n\n* [aio-pika](https://github.com/mosquito/aio-pika)\n\n',
    'author': 'Jason Watson',
    'author_email': 'jbw@jbw.cc',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/jbw/shuttle-bus',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
