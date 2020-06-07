# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['git_pr_branch',
 'git_pr_branch.servers',
 'git_pr_branch.tests',
 'git_pr_branch.utils']

package_data = \
{'': ['*']}

install_requires = \
['attrs>=19.3.0,<20.0.0',
 'click>=7.1.2,<8.0.0',
 'colorama>=0.4.3,<0.5.0',
 'python-dateutil>=2.8.1,<3.0.0',
 'requests>=2.23.0,<3.0.0']

entry_points = \
{'console_scripts': ['git-pr-branch = git_pr_branch.cli:cli']}

setup_kwargs = {
    'name': 'git-pr-branch',
    'version': '0.0.1',
    'description': 'A command line tool to manage the relationship between branches and pull-requests.',
    'long_description': "# GIT PR branch\n\n`git-pr-branch` is a command line tool designed to manage the relationship between branches and\npull-requests.\n\nAt the moment it only supports Github, but other backends are possible.\n\nYou need to create a personal token in https://github.com/settings/tokens. When you start the\nprogram for the first time, it will ask you for it and store it in a configuration file.\n\nI suggest running `git config alias.pr '!git-pr-branch'` to simplify git integration. You will just\nneed to type `git pr` to run `git-pr-branch`, options and arguments will be forwarded. With this\nalias, you can replace `git-pr-branch` with just `git pr` in the following examples.\n\n## Checking out pull requests\n\n`git-pr-branch checkout 42` will a pull request #42 in a local branch, creating a new branch each\ntime the command is run. Why, you ask? Because it is common for PR authors to amend their commits\nafter a review instead of adding more commits, and as a reviewer it's hard to see the differences\nbetween the code you reviewed and the new code. By creating a new branch each time, you can just\ndiff with the previous branch.\n\nIf you have not checked out this PR before, it will create a branch for every existing review in the\nPR's history. This way it'll be easy to see what's changed between earlier reviews even if you did\nnot run the command at that time.\n\n## Displaying branches and pull requests\n\n`git-pr-branch show` will list all your local branches and show you whether they are associated with\na pull request, whether that PR is still open or not, and the URL for that PR.\n\n## Purging branches\n\n`git-pr-branch purge` will delete the branches that are linked to a closed pull request (or multiple\npull requests that are all closed). This will let you keep your local repo tidy.\n",
    'author': 'Aurélien Bompard',
    'author_email': 'aurelien@bompard.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.com/abompard/git-pr-branch',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
