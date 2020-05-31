# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['logfmt_pandas']

package_data = \
{'': ['*']}

install_requires = \
['logfmt>=0.4,<0.5', 'pandas>=1.0.4,<2.0.0']

setup_kwargs = {
    'name': 'logfmt-pandas',
    'version': '0.1.0',
    'description': 'Read logfmt files into pandas dataframes.',
    'long_description': None,
    'author': 'Alexander Krotov',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
