# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['until']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'until',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Rafael de Oliveira Marques',
    'author_email': 'rafaelomarques@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
