# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['urp']

package_data = \
{'': ['*']}

install_requires = \
['msgpack>=1.0,<2.0']

setup_kwargs = {
    'name': 'unnamed-rpc',
    'version': '0.0.1',
    'description': 'Unnnamed PRC Protocol',
    'long_description': None,
    'author': 'Jamie Bliss',
    'author_email': 'jamie@ivyleav.es',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/minecraft-podman/urp',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
