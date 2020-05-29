# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['lowbudget2gocli']
entry_points = \
{'console_scripts': ["Packages = [{'include': 'lowbudget2gocli.py'}]",
                     'lowbudget2gocli = lowbudget2gocli:welcome_page']}

setup_kwargs = {
    'name': 'lowbudget2gocli',
    'version': '0.1.0',
    'description': 'A console program that allows developers to rea gossips, post gossips, comment and like gossips',
    'long_description': None,
    'author': 'adeayo-py',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
