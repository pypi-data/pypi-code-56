# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pysgf']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'pysgf',
    'version': '0.8.0',
    'description': 'Simple SGF parser',
    'long_description': None,
    'author': 'Sander Land',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
