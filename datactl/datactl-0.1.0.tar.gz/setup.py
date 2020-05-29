# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['datactl']

package_data = \
{'': ['*']}

install_requires = \
['fire>=0.3.1,<0.4.0',
 'pendulum>=2.1.0,<3.0.0',
 'pyyaml>=5.3.1,<6.0.0',
 'termcolor>=1.1.0,<2.0.0',
 'terminaltables>=3.1.0,<4.0.0',
 'toml>=0.10.1,<0.11.0']

entry_points = \
{'console_scripts': ['datactl = datactl.datactl:main']}

setup_kwargs = {
    'name': 'datactl',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Mohamed Cherkaoui',
    'author_email': 'chermed@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
