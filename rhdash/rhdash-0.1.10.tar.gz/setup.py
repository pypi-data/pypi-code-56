# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['rhdash']

package_data = \
{'': ['*']}

install_requires = \
['dash>=1.12.0,<2.0.0',
 'dash_auth>=1.3.2,<2.0.0',
 'pandas>=1.0.4,<2.0.0',
 'robin-stocks>=1.0.0,<2.0.0']

entry_points = \
{'console_scripts': ['rhdash = rhdash.rhdash:run']}

setup_kwargs = {
    'name': 'rhdash',
    'version': '0.1.10',
    'description': 'Dashboard for RobinHood trading',
    'long_description': None,
    'author': 'Hernando M. Vidal',
    'author_email': 'nando@hmvidal.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
