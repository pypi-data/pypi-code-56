# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['jacobi']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'jacobi',
    'version': '0.0.1',
    'description': 'Numerical derivatives',
    'long_description': None,
    'author': 'Hans Dembinski',
    'author_email': 'hans.dembinski@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
