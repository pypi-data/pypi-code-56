# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['s7', 'tests']

package_data = \
{'': ['*']}

install_requires = \
['click']

entry_points = \
{'console_scripts': ['s7 = s7.cli:main']}

setup_kwargs = {
    'name': 's7',
    'version': '0.1.0',
    'description': 'Top-level package for Seven.',
    'long_description': '=====\nSeven\n=====\n\n\n.. image:: https://img.shields.io/pypi/v/s7.svg\n        :target: https://pypi.python.org/pypi/s7\n\n.. image:: https://img.shields.io/travis/dweemx/s7.svg\n        :target: https://travis-ci.com/dweemx/s7\n\n.. image:: https://readthedocs.org/projects/s7/badge/?version=latest\n        :target: https://s7.readthedocs.io/en/latest/?badge=latest\n        :alt: Documentation Status\n\n\n.. image:: https://pyup.io/repos/github/dweemx/s7/shield.svg\n     :target: https://pyup.io/repos/github/dweemx/s7/\n     :alt: Updates\n\n\n\nPackage bundle to handle structured files\n\n\n* Free software: MIT\n* Documentation: https://s7.readthedocs.io.\n\n\nFeatures\n--------\n\n* TODO\n\nCredits\n-------\n\nThis package was created with Cookiecutter_ and the `briggySmalls/cookiecutter-pypackage`_ project template.\n\n.. _Cookiecutter: https://github.com/audreyr/cookiecutter\n.. _`briggySmalls/cookiecutter-pypackage`: https://github.com/briggySmalls/cookiecutter-pypackage\n',
    'author': 'Maxime De Waegeneer',
    'author_email': 'maxime.dewaegeneer@kuleuven.vib.be',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/dweemx/s7',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
}


setup(**setup_kwargs)
