# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['twitter_blocklist']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.2,<8.0.0', 'python-twitter>=3.5,<4.0', 'toml>=0.10.1,<0.11.0']

entry_points = \
{'console_scripts': ['twitter_blocklist = twitter_blocklist.console:main']}

setup_kwargs = {
    'name': 'twitter-blocklist',
    'version': '0.1.0',
    'description': 'Export and import Twitter blocklists',
    'long_description': None,
    'author': 'Andrea Zonca',
    'author_email': 'code@andreazonca.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
