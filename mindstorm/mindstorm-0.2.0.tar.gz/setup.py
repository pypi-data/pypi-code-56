# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mindstorm']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.18,<2.0', 'scipy>=1.4,<2.0']

setup_kwargs = {
    'name': 'mindstorm',
    'version': '0.2.0',
    'description': 'Advanced analysis of neuroimaging data',
    'long_description': None,
    'author': 'Neal Morton',
    'author_email': 'mortonne@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
