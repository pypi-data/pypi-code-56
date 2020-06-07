# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['wodonga']

package_data = \
{'': ['*']}

install_requires = \
['appdirs>=1.4.4,<2.0.0',
 'cityhash>=0.2.3,<0.3.0',
 'pytest-trio>=0.5.2,<0.6.0',
 'pytest>=5.4.2,<6.0.0',
 'structlog>=20.1.0,<21.0.0',
 'tomlkit>=0.6.0,<0.7.0',
 'trio>=0.15.1,<0.16.0']

setup_kwargs = {
    'name': 'wodonga',
    'version': '0.1',
    'description': '',
    'long_description': None,
    'author': 'Leigh Brenecki',
    'author_email': 'l@leigh.net.au',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
