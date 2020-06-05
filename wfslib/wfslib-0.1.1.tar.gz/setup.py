# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['wfslib']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['wfslib = entry:main']}

setup_kwargs = {
    'name': 'wfslib',
    'version': '0.1.1',
    'description': 'Programming module for wave front data processing',
    'long_description': None,
    'author': 'Zoya',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<3.7',
}


setup(**setup_kwargs)
