# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bgg4py', 'bgg4py.valueobject']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.2,<8.0.0',
 'devtools>=0.5.1,<0.6.0',
 'pydantic>=1.5.1,<2.0.0',
 'requests>=2.23.0,<3.0.0',
 'xmltodict>=0.12.0,<0.13.0']

setup_kwargs = {
    'name': 'bgg4py',
    'version': '0.0.1',
    'description': '',
    'long_description': '# bgg4py',
    'author': 'hiroaqii',
    'author_email': 'hiroaqii@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/hiroaqii/bgg4py',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
