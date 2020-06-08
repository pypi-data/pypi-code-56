# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aircloak_tools']

package_data = \
{'': ['*']}

install_requires = \
['pandas>=1.0.4,<2.0.0', 'psycopg2>=2.8.5,<3.0.0']

setup_kwargs = {
    'name': 'aircloak-tools',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'dlennon',
    'author_email': '3168260+dandanlen@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
