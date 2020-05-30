# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gqltype',
 'gqltype.contrib',
 'gqltype.contrib.aiohttp',
 'gqltype.contrib.connection',
 'gqltype.contrib.starlette',
 'gqltype.graphql_types',
 'gqltype.transform',
 'gqltype.utils']

package_data = \
{'': ['*']}

install_requires = \
['aniso8601', 'graphql-core']

setup_kwargs = {
    'name': 'gqltype',
    'version': '0.1.1',
    'description': 'Simple way to define GraphQL schema',
    'long_description': None,
    'author': 'miphreal',
    'author_email': 'miphreal@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<3.9',
}


setup(**setup_kwargs)
