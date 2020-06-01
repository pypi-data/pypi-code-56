# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['clypper']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.2,<8.0.0',
 'moviepy>=1.0.3,<2.0.0',
 'pytimeparse>=1.1.8,<2.0.0',
 'pytube3>=9.6.4,<10.0.0',
 'sh>=1.13.1,<2.0.0',
 'tqdm>=4.46.0,<5.0.0']

setup_kwargs = {
    'name': 'clypper',
    'version': '0.0.1',
    'description': 'Rapidly create supercuts from various video sources.',
    'long_description': None,
    'author': 'kpj',
    'author_email': 'kpjkpjkpjkpjkpjkpj@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
