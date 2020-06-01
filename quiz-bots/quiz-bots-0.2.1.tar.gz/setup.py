# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['quiz_bots']

package_data = \
{'': ['*']}

install_requires = \
['environs>=8.0.0,<9.0.0',
 'python-telegram-bot>=12.7,<13.0',
 'redis>=3.5.2,<4.0.0',
 'vk-api>=11.8.0,<12.0.0']

setup_kwargs = {
    'name': 'quiz-bots',
    'version': '0.2.1',
    'description': '',
    'long_description': None,
    'author': 'velivir',
    'author_email': 'vitaliyantonoff@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
