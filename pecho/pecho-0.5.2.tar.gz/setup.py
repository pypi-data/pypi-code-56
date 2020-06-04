# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pecho']

package_data = \
{'': ['*']}

extras_require = \
{'windows': ['colorama>=0.4.3,<0.5.0']}

setup_kwargs = {
    'name': 'pecho',
    'version': '0.5.2',
    'description': 'Easy way to write things like status bars',
    'long_description': "# pecho\n[![Tests](https://github.com/nihaals/pecho/workflows/Tests/badge.svg)](https://github.com/nihaals/pecho/actions?query=workflow%3ATests)\n[![codecov](https://codecov.io/gh/nihaals/pecho/branch/master/graph/badge.svg)](https://codecov.io/gh/nihaals/pecho)\n[![PyPI](https://img.shields.io/pypi/v/pecho)](https://pypi.org/project/pecho/)\n[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pecho)](https://pypi.org/project/pecho/)\n[![PyPI - Wheel](https://img.shields.io/pypi/wheel/pecho)](https://pypi.org/project/pecho/)\n\nPecho makes it easy to write things like status bars.\n\n## Usage\n```python\nfrom pecho import echo\n\necho('1%')  # 1%\necho('2%')  # Replaces with 2%\necho('3%', newline=True)  # Replaces with 3% and appends a newline\necho('4%')  # 3%\\n4%\n```\n",
    'author': 'Nihaal Sangha',
    'author_email': 'me@niha.al',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/nihaals/pecho',
    'packages': packages,
    'package_data': package_data,
    'extras_require': extras_require,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
