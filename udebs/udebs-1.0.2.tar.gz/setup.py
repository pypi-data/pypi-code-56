# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['udebs', 'udebs.tests']

package_data = \
{'': ['*'], 'udebs': ['keywords/*']}

setup_kwargs = {
    'name': 'udebs',
    'version': '1.0.2',
    'description': '',
    'long_description': None,
    'author': 'Ryan Chartier',
    'author_email': 'redrecrm@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
