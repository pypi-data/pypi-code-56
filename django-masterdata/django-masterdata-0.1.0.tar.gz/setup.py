# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['masterdata',
 'masterdata.importing',
 'masterdata.migrations',
 'masterdata.views']

package_data = \
{'': ['*'], 'masterdata': ['templates/admin/*', 'templates/masterdata/*']}

setup_kwargs = {
    'name': 'django-masterdata',
    'version': '0.1.0',
    'description': 'Simple data mastering tools for Django',
    'long_description': None,
    'author': 'Sebastian Acuna',
    'author_email': 'sebastian@unholster.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/unholster/django-masterdata',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
