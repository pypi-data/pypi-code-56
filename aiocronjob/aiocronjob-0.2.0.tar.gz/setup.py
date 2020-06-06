# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['aiocronjob', 'aiocronjob.webapp']

package_data = \
{'': ['*']}

install_requires = \
['crontab>=0.22.8,<0.23.0',
 'fastapi>=0.55.1,<0.56.0',
 'pytz>=2020.1,<2021.0',
 'uvicorn>=0.11.5,<0.12.0']

extras_require = \
{':python_version < "3.8"': ['importlib_metadata>=1.6.1,<2.0.0']}

setup_kwargs = {
    'name': 'aiocronjob',
    'version': '0.2.0',
    'description': '',
    'long_description': None,
    'author': 'devtud',
    'author_email': 'devtud@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
