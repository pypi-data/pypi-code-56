# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tronpy', 'tronpy.keys']

package_data = \
{'': ['*']}

install_requires = \
['base58>=2.0.0,<3.0.0',
 'ecdsa>=0.15,<0.16',
 'pycryptodome>=3.9.7,<4.0.0',
 'requests>=2.23.0,<3.0.0']

setup_kwargs = {
    'name': 'tronpy',
    'version': '0.0.1',
    'description': 'TRON Python client library',
    'long_description': None,
    'author': 'andelf',
    'author_email': 'andelf@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
