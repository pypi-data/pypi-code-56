# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['target_statistic_encoding', 'target_statistic_encoding.stat_funcs']

package_data = \
{'': ['*']}

install_requires = \
['pandas>=0.23.0,<0.24.0', 'typing_extensions>=3.7.4,<4.0.0']

setup_kwargs = {
    'name': 'target-statistic-encoding',
    'version': '0.1.1',
    'description': 'A lightweight library for encoding categorical features in your dataset with robust k-fold target statistics in training.',
    'long_description': None,
    'author': 'CircArgs',
    'author_email': 'quebecname@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
