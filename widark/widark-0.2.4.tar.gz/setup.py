# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['widark', 'widark.widget', 'widark.widget.components']

package_data = \
{'': ['*']}

install_requires = \
['aiocontextvars>=0.2.2,<0.3.0']

setup_kwargs = {
    'name': 'widark',
    'version': '0.2.4',
    'description': 'Widgets for console user interfaces',
    'long_description': None,
    'author': 'Knowark',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
