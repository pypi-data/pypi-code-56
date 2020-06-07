# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['locuplot', 'locuplot.dto', 'locuplot.helpers', 'locuplot.locust']

package_data = \
{'': ['*'], 'locuplot': ['templates/*']}

install_requires = \
['jinja2>=2.11.2,<3.0.0',
 'logzero>=1.5.0,<2.0.0',
 'matplotlib>=3.2.1,<4.0.0',
 'mpld3>=0.3,<0.4',
 'numpy>=1.18.5,<2.0.0',
 'pandas>=1.0.4,<2.0.0']

entry_points = \
{'console_scripts': ['locuplot = locuplot.main:main']}

setup_kwargs = {
    'name': 'locuplot',
    'version': '0.1.1',
    'description': 'Python application for generating plot from locust statistics csv',
    'long_description': None,
    'author': 'pawndev',
    'author_email': 'coquelet.c@gmail.com',
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
