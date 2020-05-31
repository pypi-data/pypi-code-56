# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['poethepoet', 'poethepoet.cli']

package_data = \
{'': ['*']}

install_requires = \
['poetry>=1.0.5,<2.0.0', 'toml>=0.10.1,<0.11.0']

entry_points = \
{'console_scripts': ['poe = poethepoet.cli:main']}

setup_kwargs = {
    'name': 'poethepoet',
    'version': '0.0.3',
    'description': 'A task runner that works well with poetry.',
    'long_description': "************\nPoe the Poet\n************\n\nA task runner that works well with poetry.\n\n.. role:: bash(code)\n   :language: bash\n\n.. role:: toml(code)\n   :language: toml\n\nFeatures\n========\n\n- Straight foward declaration of project tasks in your pyproject.toml (kind of like npm\n  scripts)\n- Task are run in poetry's virtualenv by default\n- Short and sweet commands with extra arguments passed to the task\n  :bash:`poe [options] task [task_args]`\n- tasks can reference environmental variables as if they were evaluated by a shell\n\nInstallation\n============\n\n.. code-block:: bash\n\n  pip install poethepoet\n\nUsage\n=====\n\nDefine tasks in your pyproject.toml\n-----------------------------------\n\n`See a real example <https://github.com/nat-n/poethepoet/blob/master/pyproject.toml>`_\n\n.. code-block:: toml\n\n  [tool.poe.tasks]\n  test = pytest --cov=poethepoet\n\nRun tasks with the poe cli\n--------------------------\n\n.. code-block:: bash\n\n  poe test\n\nAdditional argument are passed to the task so\n\n.. code-block:: bash\n\n  poe test -v tests/favorite_test.py\n\nresults in\n\n.. code-block:: bash\n\n  pytest --cov=poethepoet -v tests/favorite_test.py\n\nYou can also run it like so if you fancy\n\n.. code-block:: bash\n\n  python -m poethepoet\n\n\nRun poe from anywhere\n---------------------\n\nBy default poe will detect when you're inside a project with a pyproject.toml in the\nroot. However if you want to run it from elsewhere that is supported too by using the\n`--root` option to specify an alternate location for the toml file.\n\nBy default poe doesn't set the current workind directory to run tasks, however the\nparent directory of the toml file can be accessed as `$POE_ROOT` within the command\nline and process.\n\nPoe can also be configured to set the working directory to the project root for all\ncommands by setting :toml:`tool.poe.run_in_project_root = true` withing the\npyproject.toml.\n\nContributing\n============\n\nSure, why not?\n\nTODO\n====\n\n* make the cli more friendly with colors and supportive helpful messages\n* support running tasks outside of poetry's virtualenv (or in another?)\n* support declaring specific arguments for a task\n* test better\n* task composition/aliases\n* validate tool.poe config in toml\n* maybe try work well without poetry too\n\nLicence\n=======\n\nMIT. Go nuts.\n",
    'author': 'Nat Noordanus',
    'author_email': 'n@natn.me',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/nat-n/poethepoet',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
