# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pengu', 'pengu.cloud']

package_data = \
{'': ['*']}

install_requires = \
['mypy>=0.780,<0.781', 'tensorflow==2.2.0']

extras_require = \
{'test': ['pytest[test]>=5.4.3,<6.0.0',
          'pytest-cov[test]>=2.9.0,<3.0.0',
          'flake8[test]>=3.8.2,<4.0.0']}

setup_kwargs = {
    'name': 'pengu',
    'version': '0.0.1',
    'description': 'WIP',
    'long_description': '\n# Pengu: a Library for Deep Learning in Computer Vision\nWork In Progress！\n\n![Test](https://github.com/peachanG/pengu/workflows/Test/badge.svg?branch=master)\n![Python](https://img.shields.io/badge/python-3.7%20%7C%203.8-blue?logo=python)\n[![GitHub Issues](https://img.shields.io/github/issues/peachanG/pengu.svg?cacheSeconds=60&color=yellow)](https://github.com/peachanG/pengu/issues)\n[![GitHub Pull Requests](https://img.shields.io/github/issues-pr/peachanG/pengu.svg?cacheSeconds=60&color=yellow)](https://github.com/peachanG/pengu/issues)\n[![GitHub Release](https://img.shields.io/github/release/peachanG/pengu.svg?cacheSeconds=60&color=red)](https://github.com/peachanG/pengu/releases)',
    'author': 'peachanG',
    'author_email': 'kenkman0427@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/peachanG',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7.6,<4.0.0',
}


setup(**setup_kwargs)
