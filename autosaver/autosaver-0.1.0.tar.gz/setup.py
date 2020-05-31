# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['autosaver', 'autosaver.banks']

package_data = \
{'': ['*']}

install_requires = \
['requests-oauthlib>=1.3.0,<2.0.0']

setup_kwargs = {
    'name': 'autosaver',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Richard Morrison',
    'author_email': 'richard@rmorrison.net',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
