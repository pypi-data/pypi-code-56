# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['creativeai']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'creativeai',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Alex J. Champandard',
    'author_email': '445208+alexjc@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
