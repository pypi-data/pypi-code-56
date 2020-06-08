# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['vidgen']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.2,<8.0.0', 'praw>=7.0.0,<8.0.0', 'requests>=2.23.0,<3.0.0']

extras_require = \
{':python_version < "3.8"': ['importlib_metadata>=1.6.0,<2.0.0']}

entry_points = \
{'console_scripts': ['vidgen = vidgen.console:cli']}

setup_kwargs = {
    'name': 'vidgen',
    'version': '0.2.0',
    'description': 'Automatic video generation',
    'long_description': '# vidgen\n![Tests](https://github.com/Scoder12/vidgen/workflows/Tests/badge.svg)\n[![codecov](https://codecov.io/gh/Scoder12/vidgen/branch/master/graph/badge.svg)](https://codecov.io/gh/Scoder12/vidgen)\n[![PyPi](https://img.shields.io/pypi/v/vidgen)](https://pypi.org/p/vidgen)\n\nAutomatic video generation\n',
    'author': 'Your Name',
    'author_email': 'you@example.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
