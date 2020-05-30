# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['cli', 'utils', 'readme', 'requirements', '.env']
install_requires = \
['colorama>=0.4.3,<0.5.0',
 'pusher>=3.0.0,<4.0.0',
 'pysher>=1.0.6,<2.0.0',
 'termcolor>=1.1.0,<2.0.0']

entry_points = \
{'console_scripts': ['devgossip-v2 = cli:welcome']}

setup_kwargs = {
    'name': 'devgossip-v2',
    'version': '2.4.1',
    'description': 'About: devGossip is a commandline forum app for interaction between developers from around the world. It is a safe space for developers to talk about anything and everything. Users can signup, join any room of their choice to interact with other developers and they also have the option to delete their account. Conversations are not saved to give you the freedom to say all you want.',
    'long_description': None,
    'author': 'Mark Okhakumhe',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
