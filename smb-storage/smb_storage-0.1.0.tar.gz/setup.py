# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['smb_storage']
install_requires = \
['pysmb>=1.2.1,<2.0.0']

setup_kwargs = {
    'name': 'smb-storage',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'pat-rapidai',
    'author_email': 'sheehan@rapid.ai',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=2.7,<3.0',
}


setup(**setup_kwargs)
