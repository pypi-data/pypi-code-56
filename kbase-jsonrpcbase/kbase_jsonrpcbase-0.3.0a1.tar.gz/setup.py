# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['jsonrpcbase']

package_data = \
{'': ['*']}

install_requires = \
['jsonschema>=3.2.0,<4.0.0', 'pytest-cov>=2.9.0,<3.0.0']

setup_kwargs = {
    'name': 'kbase-jsonrpcbase',
    'version': '0.3.0a1',
    'description': 'Simple JSON-RPC service without transport layer',
    'long_description': None,
    'author': None,
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/kbaseIncubator/jsonrpcbase',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
