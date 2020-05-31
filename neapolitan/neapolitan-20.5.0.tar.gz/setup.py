# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['neapolitan']

package_data = \
{'': ['*']}

install_requires = \
['Django>=3.0.6,<4.0.0']

setup_kwargs = {
    'name': 'neapolitan',
    'version': '20.5.0',
    'description': '',
    'long_description': None,
    'author': 'Carlton Gibson',
    'author_email': 'carlton.gibson@noumenal.es',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
