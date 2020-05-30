# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['damy_program']

package_data = \
{'': ['*']}

install_requires = \
['python-string-utils>=1.0.0,<2.0.0', 'requests>=2.23.0,<3.0.0']

setup_kwargs = {
    'name': 'damy-program',
    'version': '0.1.1',
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
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
