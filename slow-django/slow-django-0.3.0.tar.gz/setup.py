# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['slow_django']

package_data = \
{'': ['*']}

install_requires = \
['django>=3.0.7,<4.0.0']

setup_kwargs = {
    'name': 'slow-django',
    'version': '0.3.0',
    'description': '',
    'long_description': None,
    'author': 'Your Name',
    'author_email': 'you@example.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
