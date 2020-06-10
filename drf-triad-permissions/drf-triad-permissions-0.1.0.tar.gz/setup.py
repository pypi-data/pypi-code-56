# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['drf_triad_permissions']

package_data = \
{'': ['*'], 'drf_triad_permissions': ['templates/drf_triad_permissions/*']}

install_requires = \
['django>=2.0,<4.0', 'djangorestframework>=3.11.0,<4.0.0']

setup_kwargs = {
    'name': 'drf-triad-permissions',
    'version': '0.1.0',
    'description': 'DRF viewset permissions through triads',
    'long_description': None,
    'author': 'Lorenzo Peña',
    'author_email': 'lorinkoz@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
