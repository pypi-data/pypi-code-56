# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

modules = \
['enciphey']
setup_kwargs = {
    'name': 'enciphey',
    'version': '0.1.0',
    'description': 'Randomly chooses an encryption',
    'long_description': None,
    'author': 'Brandon',
    'author_email': 'brandon@skerritt.blog',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'py_modules': modules,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
