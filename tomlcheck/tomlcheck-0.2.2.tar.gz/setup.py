# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tomlcheck']

package_data = \
{'': ['*']}

install_requires = \
['toml>=0.10.0,<0.11.0']

entry_points = \
{'console_scripts': ['tomlcheck = tomlcheck.run:run']}

setup_kwargs = {
    'name': 'tomlcheck',
    'version': '0.2.2',
    'description': 'A simple toml syntax checker',
    'long_description': 'tomlcheck\n==========\n\n.. image:: https://img.shields.io/pypi/v/tomlcheck.svg\n    :target: https://pypi.org/project/tomlcheck\n    :alt:\n\n.. image:: https://img.shields.io/pypi/pyversions/tomlcheck.svg\n    :target: https://pypi.org/project/tomlcheck\n    :alt:\n\n.. image:: https://travis-ci.com/sayanarijit/tomlcheck.svg?branch=master\n    :target: https://travis-ci.com/sayanarijit/tomlcheck\n    :alt:\n\n.. image:: https://codecov.io/gh/sayanarijit/tomlcheck/branch/master/graph/badge.svg\n    :target: https://codecov.io/gh/sayanarijit/tomlcheck\n    :alt:\n\n.. image:: https://img.shields.io/badge/code%20style-black-000000.svg\n    :target: https://github.com/python/black\n    :alt:\n\n\nA simple toml syntax checker.\n\nDesigned to be used by `pre-commit <https://github.com/pre-commit/pre-commit>`_ hooks.\n\n\nInstallation\n------------\n\n.. code-block:: bash\n\n    pip install -U tomlcheck\n\n\nUsage\n-----\n\nCheck files:\n\n.. code-block:: bash\n\n    tomlcheck $(find . -type f -name "*.toml")\n\n    # Or read from stdin\n\n    find . -type f -name "*.toml" | tomlcheck -\n\n\nWith logging:\n\n.. code-block:: bash\n\n    tomlcheck --log-level DEBUG $(find . -type f -name "*.toml")\n    \n    # Or read from stdin\n\n    find . -type f -name "*.toml" | tomlcheck --log-level DEBUG -\n\nIn `pre-commit <https://github.com/pre-commit/pre-commit>`_ config:\n\n.. code-block:: yaml\n\n    # .pre-commit-config.yaml\n\n    - repo: local\n      hooks:\n      - id: tomlcheck\n        name: Check TOML Syntax\n        description: Checks TOML files for valid syntax.\n        entry: tomlcheck\n        language: system\n        files: \\**/*.toml$\n        stages: [commit, push, manual]\n\n\nHelp Menu\n---------\n\n.. code-block:: bash\n\n    tomlcheck --help\n',
    'author': 'Arijit Basu',
    'author_email': 'sayanarijit@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'http://github.com/sayanarijit/tomlcheck',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
