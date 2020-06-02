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
    'version': '0.2.1',
    'description': 'A tool to backup and delete the content of private slack channels',
    'long_description': "\nSlack Secret\n=============\n\nInstallation::\n\n    pip install slack-secret\n\n\n\nDevelopement\n=============\n\nThese instructions assume that you've installed the following tools:\n\n* `Pyenv <https://github.com/pyenv/pyenv>`_\n* `Pyenv-virtualenv <https://github.com/pyenv/pyenv-virtualenv>`_\n* `Poetry <https://python-poetry.org/>`_\n* `Pre-commit <https://pre-commit.com/>`_\n\n1. Create a virtualenv\n\npyenv virtualenv 3.8.1 slacksecret\n\n2. Install pre-commit\n\n\nCheck the doc on\n\nOr::\n\n    pip install pre-commit\n    pre-commit install\n    pre-commit run --all-files\n\nGetting started\n===============\n\npyenv virtualenv 3.8.1 slacksecret\n\n\nUsing poetry 101\n\n\nManaging the environment\n\npoetry add <library-name>\npoetry install: install all the libraries\npeoetry update: update the dependecies\npoetry version [major-minor-patch]\n\nPublishing\n\npoetry publish --build\n\ntype login and password\n",
    'author': 'Nicolas Paris',
    'author_email': 'ni.paris@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/niparis/slack-secret',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
