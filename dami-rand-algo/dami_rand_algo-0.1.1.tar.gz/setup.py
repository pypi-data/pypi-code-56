# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['dami_rand_algo']
install_requires = \
['python-string-utils>=1.0.0,<2.0.0', 'requests>=2.23.0,<3.0.0']

entry_points = \
{'console_scripts': ['dami_rand_algo = entry:main']}

setup_kwargs = {
    'name': 'dami-rand-algo',
    'version': '0.1.1',
    'description': 'A CLI based program that randomly fetches questions and answers from an API and returns it to the user.',
    'long_description': None,
    'author': 'Oluwadamilola Sonaike',
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
