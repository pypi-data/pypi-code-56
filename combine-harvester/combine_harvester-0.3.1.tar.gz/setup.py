# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['utils']
install_requires = \
['click>=7.1.2,<8.0.0',
 'iso8601>=0.1.12,<0.2.0',
 'pyfzf>=0.2.1,<0.3.0',
 'requests>=2.23.0,<3.0.0']

entry_points = \
{'console_scripts': ['harvest = combine_harvester:main']}

setup_kwargs = {
    'name': 'combine-harvester',
    'version': '0.3.1',
    'description': 'CLI tool to log Harvest timesheets with FZF ',
    'long_description': "# Combine Harvester\n\nCLI tool to log [Harvest](https://www.getharvest.com/) timesheets with FZF\n\n![PyPI - Python Version](https://img.shields.io/pypi/pyversions/combine_harvester) [![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n\n## Requirements\n\n* At least python 3.6 (sorry, I just like f-strings a bit too much)\n* [fzf](https://github.com/junegunn/fzf)\n\n## Installation\n\n```\npip install combine-harvester\n```\n\n## Environment Variables\n\nTwo variables need to be in your environment to authenticate yourself to Harvest's API.\n\n* HARVEST_ACCOUNT_ID\n* HARVEST_ACCOUNT_TOKEN\n\nCreating these tokens can be done through [Harvest's Developer Tools](https://id.getharvest.com/developers) page.\n\n## Usage\n\nThis [wiki page](https://github.com/BamBalaam/combine-harvester/wiki/Usage) lists all commands and their usage.\n\n```\n> harvest\n\nUsage: harvest [OPTIONS] COMMAND [ARGS]...\n\n  Combine Harvester is a Harvest CLI Tool\n\nOptions:\n  --help  Show this message and exit.\n\nCommands:\n  daily  Get notes from previous work day, to be used during daily standup.\n  list   Get time entries from today, or optionally another day.\n  log    Log time entry for today, using FZF.\n```\n\n## Disclaimer\n\nThis tool is not an official [Harvest](https://www.getharvest.com/) tool, nor am I affiliated to them.\n",
    'author': 'André Madeira Cortes',
    'author_email': 'amadeiracortes@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/BamBalaam/combine-harvester',
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
