# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['combine_harvester']
install_requires = \
['jq>=1.0.1,<2.0.0', 'pyfzf>=0.2.1,<0.3.0', 'requests>=2.23.0,<3.0.0']

entry_points = \
{'console_scripts': ['harvest = combine_harvester:main']}

setup_kwargs = {
    'name': 'combine-harvester',
    'version': '0.1.1',
    'description': '',
    'long_description': '# Combine Harvester\n\nCLI tool to log Harvest timesheets with FZF\n\n## Installation \n\n```\npip install combine-harvester\n```\n\n## Requirements\n\n* Python 3.6 (f-strings!)\n* [jq](https://github.com/stedolan/jq)\n* [fzf](https://github.com/junegunn/fzf)\n\n## Environment Variables\n\n* HARVEST_ACCOUNT_ID\n* HARVEST_ACCOUNT_TOKEN\n\n## Usage\n\n```\n> harvest\n```\n',
    'author': 'André Madeira Cortes',
    'author_email': 'amadeiracortes@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
