# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['tsdoc', 'tsdoc.python']

package_data = \
{'': ['*']}

install_requires = \
['attrs>=19.3.0,<20.0.0', 'textx_ls_core>=0.1.1,<0.2.0']

entry_points = \
{'textx_languages': ['tsdoc.python = tsdoc.python:register']}

setup_kwargs = {
    'name': 'tsdoc',
    'version': '0.1.1',
    'description': 'TSDoc is an embedded comment language for TechSmart code files.',
    'long_description': None,
    'author': 'Ryan Sobol',
    'author_email': 'ryan.sobol@techsmart.codes',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
