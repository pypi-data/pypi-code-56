# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['zeroed']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.1,<8.0.0', 'docopt>=0.6.2,<0.7.0']

entry_points = \
{'console_scripts': ['zeroed = zeroed.cli:main']}

setup_kwargs = {
    'name': 'zeroed',
    'version': '0.1.0rc1',
    'description': 'Zeroed is a CLI package for resetting trash and apps to the settings of certain apps on Linux.',
    'long_description': '.. image:: https://github.com/snakypy/zeroed/workflows/Python%20package/badge.svg\n    :target: https://github.com/snakypy/zeroed\n\n.. image:: https://img.shields.io/pypi/v/zeroed.svg\n    :target: https://pypi.python.org/pypi/zeroed\n\n.. image:: https://travis-ci.com/snakypy/zeroed.svg?branch=master\n    :target: https://travis-ci.com/snakypy/zeroed\n\n.. image:: https://img.shields.io/pypi/wheel/zeroed\n    :alt: PyPI - Wheel\n\n.. image:: https://img.shields.io/badge/code%20style-black-000000.svg\n    :target: https://github.com/psf/black\n\n.. image:: https://pyup.io/repos/github/snakypy/zeroed/shield.svg\n    :target: https://pyup.io/repos/github/snakypy/zeroed/\n    :alt: Updates\n\n.. image:: https://img.shields.io/github/issues-raw/snakypy/zeroed\n    :alt: GitHub issues\n\n.. image:: https://img.shields.io/github/license/snakypy/zeroed\n    :alt: GitHub license\n    :target: https://github.com/snakypy/zeroed/blob/master/LICENSE\n\nRequirements\n------------\n\nTo work correctly, you will first need:\n\n* `python`_ (v3.8 or recent) must be installed.\n* `pip`_ (v20.0 or recent) must be installed.\n\nInstalling\n----------\n\nGlobally:\n\n.. code-block:: shell\n\n    $ sudo pip install zeroed\n\nFor the user:\n\n.. code-block:: shell\n\n    $ pip install zeroed --user\n\n\nUsing\n-----\n\nAccess the official page of the project where you can find a description of use:\n\n\nThe gem is available as open source under the terms of the `MIT License`_ ©\n\nCredits\n-------\n\nSee, `AUTHORS`_.\n\nLinks\n-----\n\n* Code: https://github.com/snakypy/zeroed\n* Documentation: https://github.com/snakypy/zeroed/blob/master/README.md\n* Releases: https://pypi.org/project/zeroed/#history\n* Issue tracker: https://github.com/snakypy/zeroed/issues\n\n.. _AUTHORS: https://github.com/snakypy/zeroed/blob/master/AUTHORS.rst\n.. _python: https://python.org\n.. _pip: https://pip.pypa.io/en/stable/quickstart/\n.. _MIT License: https://github.com/snakypy/zeroed/blob/master/LICENSE\n',
    'author': 'William C. Canin',
    'author_email': 'william.costa.canin@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/snakypy/zeroed',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
