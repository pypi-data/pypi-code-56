# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['testpoetry']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'testpoetry',
    'version': '0.1.4',
    'description': '',
    'long_description': None,
    'author': 'Firastic',
    'author_email': 'adyaksa.wisanggeni@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
