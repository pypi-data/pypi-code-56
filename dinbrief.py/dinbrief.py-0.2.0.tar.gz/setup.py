# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['dinbrief']
install_requires = \
['click>=7.1.1,<8.0.0',
 'click_default_group>=1.2.2,<2.0.0',
 'click_log>=0.3.2,<0.4.0',
 'crayons>=0.3.0,<0.4.0',
 'delegator.py>=0.1.1,<0.2.0',
 'halo>=0.0.29,<0.0.30',
 'pyyaml>=5.3.1,<6.0.0']

setup_kwargs = {
    'name': 'dinbrief.py',
    'version': '0.2.0',
    'description': 'Dinbrief made easy',
    'long_description': None,
    'author': 'Markus Quade',
    'author_email': 'info@markusqua.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
