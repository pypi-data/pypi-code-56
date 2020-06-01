# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['zealous', 'zealous.rpc', 'zealous.rpc.asyncioq', 'zealous.schema']

package_data = \
{'': ['*']}

install_requires = \
['pydantic>=1.4,<2.0']

setup_kwargs = {
    'name': 'zealous',
    'version': '0.2.2',
    'description': 'Zealous Framework',
    'long_description': None,
    'author': 'Jonathan Gravel',
    'author_email': 'jo@stashed.dev',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
