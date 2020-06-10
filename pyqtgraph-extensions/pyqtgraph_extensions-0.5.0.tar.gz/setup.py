# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyqtgraph_extensions',
 'pyqtgraph_extensions.examples',
 'pyqtgraph_extensions.opengl',
 'pyqtgraph_extensions.opengl.test',
 'pyqtgraph_extensions.test']

package_data = \
{'': ['*']}

install_requires = \
['PyQt5>=5.14.2,<6.0.0',
 'mathx>=0.2.0,<0.3.0',
 'pyopengl>=3.1.5,<4.0.0',
 'pyqtgraph==0.11.0']

setup_kwargs = {
    'name': 'pyqtgraph-extensions',
    'version': '0.5.0',
    'description': 'Various extensions for pyqtgraph.',
    'long_description': None,
    'author': 'Dane Austin',
    'author_email': 'dane_austin@fastmail.com.au',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
