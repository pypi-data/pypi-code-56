# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['platform_metrics']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'platform-metrics',
    'version': '0.1.0a1.dev1',
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
