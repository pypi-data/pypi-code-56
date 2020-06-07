# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pavlov']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'async-pavlov',
    'version': '0.1.1',
    'description': 'Async wrapper for Pavlov VR RCON commands',
    'long_description': '# async-pavlov\nAsync wrapper for pavlov RCON commands\n',
    'author': 'makubob',
    'author_email': 'makupi@icloud.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/makupi/async-pavlov',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
