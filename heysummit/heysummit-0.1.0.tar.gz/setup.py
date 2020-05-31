# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['heysummit']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.23.0,<3.0.0']

setup_kwargs = {
    'name': 'heysummit',
    'version': '0.1.0',
    'description': 'HeySummit API Client',
    'long_description': None,
    'author': 'Felipe Zipitria',
    'author_email': 'felipe.zipitria@owasp.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
