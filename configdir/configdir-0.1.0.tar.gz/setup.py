# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['configdir']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'configdir',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Michael Thornton',
    'author_email': 'six8@devdetails.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*, !=3.5.*',
}


setup(**setup_kwargs)
