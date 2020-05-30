# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['job_house']
entry_points = \
{'console_scripts': ['job_alert = job_house:home']}

setup_kwargs = {
    'name': 'job-alert',
    'version': '0.1.0',
    'description': 'job alert is an application that employers logs in and post job offers and job seekers logs in to see jobs posted',
    'long_description': None,
    'author': 'Andrew Gabriel',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'entry_points': entry_points,
    'python_requires': '>3.0',
}


setup(**setup_kwargs)
