# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fbchatbot', 'fbchatbot.base_plugin']

package_data = \
{'': ['*']}

install_requires = \
['attr>=0.3.1,<0.4.0', 'fbchat==2.0.0a2']

setup_kwargs = {
    'name': 'fbchatbot',
    'version': '0.1.0',
    'description': 'Easily define chatbots for Facebook Messenger',
    'long_description': None,
    'author': 'Matthew Wetmore',
    'author_email': 'wetmore.matt@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
