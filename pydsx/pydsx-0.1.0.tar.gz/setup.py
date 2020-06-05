# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pydsx', 'pydsx.binary_search_tree', 'pydsx.singly_linked_list']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'pydsx',
    'version': '0.1.0',
    'description': 'Data structures in python to use in some projects <Matheus Francisco>',
    'long_description': None,
    'author': 'matheusfrancisco',
    'author_email': 'matheusmachadoufsc@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
