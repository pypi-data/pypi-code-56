# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyture_remo']

package_data = \
{'': ['*'], 'pyture_remo': ['testdata/*']}

install_requires = \
['requests>=2.23.0,<3.0.0']

setup_kwargs = {
    'name': 'pyture-remo',
    'version': '0.2.2',
    'description': 'nature-remo library for Python',
    'long_description': None,
    'author': 'Suzuka Asagiri',
    'author_email': 'admin@suzutan.jp',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
