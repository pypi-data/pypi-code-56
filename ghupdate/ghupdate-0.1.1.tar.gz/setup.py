# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ghupdate',
 'ghupdate.controllers',
 'ghupdate.core',
 'ghupdate.ext',
 'ghupdate.plugins']

package_data = \
{'': ['*']}

install_requires = \
['cement>=3.0.4,<4.0.0',
 'colorlog>=4.1.0,<5.0.0',
 'jinja2>=2.11.2,<3.0.0',
 'pygithub>=1.51,<2.0',
 'pyyaml>=5.3.1,<6.0.0',
 'rich>=1.2.3,<2.0.0']

setup_kwargs = {
    'name': 'ghupdate',
    'version': '0.1.1',
    'description': '',
    'long_description': None,
    'author': 'Dimitrios Strantsalis',
    'author_email': 'dstrants@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
