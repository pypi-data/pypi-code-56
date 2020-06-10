# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['requires']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'requires',
    'version': '0.0.1',
    'description': '',
    'long_description': None,
    'author': 'sheldon-turtle',
    'author_email': 'sheldon@dgi.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
