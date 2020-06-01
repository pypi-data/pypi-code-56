# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['svg_tools']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.18.4,<2.0.0']

setup_kwargs = {
    'name': 'blue-dot-sessions-svg-tools',
    'version': '0.4.0',
    'description': 'SVG tools for Blue Dot Sessions',
    'long_description': None,
    'author': 'Dean Shaff',
    'author_email': 'dean.shaff@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
