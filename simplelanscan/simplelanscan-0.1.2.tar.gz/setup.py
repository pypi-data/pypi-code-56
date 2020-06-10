# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['simplelanscan']

package_data = \
{'': ['*']}

install_requires = \
['elasticsearch>=7.0.0,<8.0.0', 'scapy==2.4.3']

setup_kwargs = {
    'name': 'simplelanscan',
    'version': '0.1.2',
    'description': 'Python Script to scan the local lan and report back the clients currently connected.',
    'long_description': None,
    'author': 'blcarlson01',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
