# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['combine_harvester']
install_requires = \
['jq>=1.0.1,<2.0.0', 'pyfzf>=0.2.1,<0.3.0', 'requests>=2.23.0,<3.0.0']

entry_points = \
{'console_scripts': ['harvest = combine_harvester:main']}

setup_kwargs = {
    'name': 'combine-harvester',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'André Madeira Cortes',
    'author_email': 'amadeiracortes@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
