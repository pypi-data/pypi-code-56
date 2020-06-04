# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['moic',
 'moic.cli',
 'moic.cli.commands',
 'moic.cli.commands.context',
 'moic.cli.commands.issue',
 'moic.cli.commands.rabbit',
 'moic.cli.commands.resources',
 'moic.cli.commands.template',
 'moic.cli.completion',
 'moic.cli.utils',
 'moic.cli.validators',
 'moic.plugins',
 'moic.plugins.jira',
 'moic.plugins.jira.commands',
 'moic.plugins.jira.commands.issue',
 'moic.plugins.jira.commands.resources',
 'moic.plugins.jira.commands.sprint',
 'moic.plugins.jira.completion',
 'moic.plugins.jira.utils',
 'moic.plugins.jira.validators']

package_data = \
{'': ['*']}

install_requires = \
['antidote>=0.7.0,<0.8.0',
 'click>=7.1.1,<8.0.0',
 'commonmark>=0.9.1,<0.10.0',
 'dynaconf>=2.2.3,<3.0.0',
 'jira',
 'keyring>=21.1.1,<22.0.0',
 'pyyaml>=5.3,<6.0',
 'rich>=0.8.8,<0.9.0',
 'tomd>=0.1.3,<0.2.0']

entry_points = \
{'console_scripts': ['moic = moic.base:run']}

setup_kwargs = {
    'name': 'moic',
    'version': '1.3.1',
    'description': 'My Own Issue CLI (Jira, Gitlab etc...)',
    'long_description': '# MOIC : My Own Issue CLI\n\n> Freely inspired by https://pypi.org/project/jira-cli/\n\nCommand line inteface to interact with issue manager such as Jira, Gitlab, etc...\n\n**Highlights**\n* Modern CLI based on [Click](https://click.palletsprojects.com/en/7.x/) and [Rich](https://github.com/willmcgugan/rich)\n* Context management\n* Multiple tracker plugin\n* Uniformed display\n\n## Getting Started\n\n* Install moic\n```bash\n> pip install moic\n```\n\n* Configure moic\n```bash\n> moic configure\n```\n\n* Commands\n```bash\n> moic\nUsage: moic [OPTIONS] COMMAND [ARGS]...\n\nOptions:\n  --help  Show this message and exit.\n\nCommands:\n  config    Configure Jira cli, setting up instance, credentials etc...\n  issue     Create, edit, list Jira issues\n  list      List projects, issue_types, priorities, status\n  rabbit    Print an amazing rabbit: Tribute to @fattibenji...\n  sprint    Create, edit, list Jira Sprints\n  template  List, edit templates\n  version   Provide the current moic installed version\n```\n\n## Contribute\n\nFeel free [open issues on Gitlab](https://gitlab.com/brice.santus/moic/-/issues) or propose Merge Requests\n\n## Documentation\n\nFull documentation is available at https://moic.readthedocs.io/en/latest/\n',
    'author': 'Brice Santus',
    'author_email': 'brice.santus@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://moic.readthedocs.io/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
