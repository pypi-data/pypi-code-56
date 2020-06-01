# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['wdlkit']

package_data = \
{'': ['*'], 'wdlkit': ['templates/*']}

install_requires = \
['autoclick>=0.8.1,<0.9.0', 'miniwdl>=0.7.0,<0.8.0', 'networkx>=2.4,<3.0']

entry_points = \
{'console_scripts': ['wdlkit = wdlkit.__main__:wdlkit']}

setup_kwargs = {
    'name': 'wdlkit',
    'version': '0.0.post14',
    'description': 'WDL development tools',
    'long_description': None,
    'author': 'John Didion',
    'author_email': 'jdidion@dnanexus.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
