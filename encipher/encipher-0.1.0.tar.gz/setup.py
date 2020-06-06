# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

modules = \
['encipher']
setup_kwargs = {
    'name': 'encipher',
    'version': '0.1.0',
    'description': 'Randomly encrypts text',
    'long_description': None,
    'author': 'Brandon',
    'author_email': 'brandonskerritt51@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'py_modules': modules,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
