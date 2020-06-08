# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['delb_reference_plugins']

package_data = \
{'': ['*']}

install_requires = \
['delb==0.2b3']

entry_points = \
{'delb': ['custom-loader = delb_reference_plugins.custom_loader',
          'header-properties = delb_reference_plugins.header_properties']}

setup_kwargs = {
    'name': 'delb-reference-plugins',
    'version': '0.2b3',
    'description': "A package with spare non-sense plugins for delb as developer's reference.",
    'long_description': None,
    'author': 'Frank Sachsenheim',
    'author_email': 'funkyfuture@riseup.net',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<3.7',
}


setup(**setup_kwargs)
