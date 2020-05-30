# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['lowbudget2gocli']
entry_points = \
{'console_scripts': ['lowbudget_2go_cli = lowbudget2gocli:database']}

setup_kwargs = {
    'name': 'lowbudget-2go-cli',
    'version': '0.1.0',
    'description': 'A command line application that allows developers post, read, comment and like gossips',
    'long_description': None,
    'author': 'Adeayo',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'entry_points': entry_points,
    'python_requires': '>3.0',
}


setup(**setup_kwargs)
