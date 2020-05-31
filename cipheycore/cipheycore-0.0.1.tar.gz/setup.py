# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cipheycore']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'cipheycore',
    'version': '0.0.1',
    'description': '',
    'long_description': None,
    'author': 'Cyclic3',
    'author_email': 'cyclic3.git@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
