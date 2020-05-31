# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pygeojson']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'pygeojson',
    'version': '0.1.0',
    'description': 'GeoJSON library for Python with types',
    'long_description': None,
    'author': 'Håkon Åmdal',
    'author_email': 'hakon@aamdal.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
