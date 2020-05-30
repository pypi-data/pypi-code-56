# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['migrate']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'nimbus-migrate',
    'version': '0.1.0',
    'description': 'A simple migration library for nimbus cloud apps and services',
    'long_description': None,
    'author': 'Zach Bullough',
    'author_email': 'zbullough@qmulosoft.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
