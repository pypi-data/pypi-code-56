# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['majority_judgment']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'majority-judgment',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'mieuxvoter contributors',
    'author_email': 'contact@mieuxvoter.fr',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
