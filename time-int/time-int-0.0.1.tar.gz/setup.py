# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['time_int']

package_data = \
{'': ['*']}

install_requires = \
['pytest>=5.4.2,<6.0.0']

setup_kwargs = {
    'name': 'time-int',
    'version': '0.0.1',
    'description': 'Subclass of integer representing seconds since UNIX epoch',
    'long_description': None,
    'author': 'Andrew Allaire',
    'author_email': 'andrew.allaire@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
