# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['platform_logging']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'platform-logging',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Edward George',
    'author_email': 'edward.george@maersk.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=2.7,<3.0',
}


setup(**setup_kwargs)
