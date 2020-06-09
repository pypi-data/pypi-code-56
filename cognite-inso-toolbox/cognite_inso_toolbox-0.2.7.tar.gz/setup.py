# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': '.'}

packages = \
['inso_toolbox', 'inso_toolbox.utils']

package_data = \
{'': ['*']}

install_requires = \
['cognite-sdk-experimental>=0.11.0,<0.12.0']

setup_kwargs = {
    'name': 'cognite-inso-toolbox',
    'version': '0.2.7',
    'description': 'Inso Toolbox',
    'long_description': None,
    'author': 'cognite',
    'author_email': 'gustavo.zarruk@cognite.com, nicholas.calen@cognite.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
