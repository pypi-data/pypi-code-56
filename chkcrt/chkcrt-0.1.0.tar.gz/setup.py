# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['chkcrt']

package_data = \
{'': ['*']}

install_requires = \
['cryptography>=2.9.2,<3.0.0', 'slackclient>=2.6.1,<3.0.0']

entry_points = \
{'console_scripts': ['chkcrt = chkcrt.__main__:main']}

setup_kwargs = {
    'name': 'chkcrt',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Naglis Jonaitis',
    'author_email': 'hello@naglis.me',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
