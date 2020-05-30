# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['Fake_job', 'jobs', 'User_Data']
entry_points = \
{'console_scripts': ['Itarj_app = Fake_job:choices']}

setup_kwargs = {
    'name': 'itarj-app',
    'version': '1.0.0',
    'description': 'ITARJ CONSOLE: A console app that allows users to register fake job alerts and allows others to view those posts by searching for keywords.',
    'long_description': 'this is the initial readnme file\n',
    'author': 'Emmanuel Chijioke aka DREL',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'entry_points': entry_points,
    'python_requires': '>=2.0,<3.0',
}


setup(**setup_kwargs)
