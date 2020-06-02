# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['slack_secret']

package_data = \
{'': ['*']}

install_requires = \
['slackclient>=2.6.2,<3.0.0', 'tqdm>=4.46.0,<5.0.0']

entry_points = \
{'console_scripts': ['slacksecrets = slack_secret.main:cli']}

setup_kwargs = {
    'name': 'slack-secret',
    'version': '0.2.0',
    'description': '',
    'long_description': None,
    'author': 'Nicolas Paris',
    'author_email': 'ni.paris@gmail.com',
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
