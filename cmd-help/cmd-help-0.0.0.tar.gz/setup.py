# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['src']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'cmd-help',
    'version': '0.0.0',
    'description': '',
    'long_description': '# cmd-help',
    'author': 'guaifish',
    'author_email': 'guaifish@foxmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/guaifish/cmd-help',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
