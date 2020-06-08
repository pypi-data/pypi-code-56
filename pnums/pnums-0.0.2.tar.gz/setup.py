# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pnums']

package_data = \
{'': ['*']}

install_requires = \
['numpy==1.16.1', 'scipy>=1.4.1,<2.0.0']

setup_kwargs = {
    'name': 'pnums',
    'version': '0.0.2',
    'description': 'A library that encodes coordinates so neural networks can use them better.',
    'long_description': 'PCoords\n=======\nNeural Coordinates\n\nInstallation\n------------\nWill be pip installable on first release.',
    'author': 'SimLeek',
    'author_email': 'simulator.leek@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/simleek/pnums',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
