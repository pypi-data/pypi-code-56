# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['pocket_recommendations']
install_requires = \
['cssselect>=1.1.0,<2.0.0', 'lxml>=4.5.1,<5.0.0']

setup_kwargs = {
    'name': 'pocket-recommendations',
    'version': '0.1.0',
    'description': "Unofficial library to get a feed of one's Pocket recommendations",
    'long_description': None,
    'author': 'Honza Javorek',
    'author_email': 'mail@honzajavorek.cz',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
