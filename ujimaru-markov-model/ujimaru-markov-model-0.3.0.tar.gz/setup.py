# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ujimaru_markov_model']

package_data = \
{'': ['*']}

install_requires = \
['markovify>=0.8.0,<0.9.0']

entry_points = \
{'console_scripts': ['ujimaru = ujimaru_markov_model.cli:main']}

setup_kwargs = {
    'name': 'ujimaru-markov-model',
    'version': '0.3.0',
    'description': '',
    'long_description': None,
    'author': 'hppRC',
    'author_email': 'hpp.ricecake@gmail.com',
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
