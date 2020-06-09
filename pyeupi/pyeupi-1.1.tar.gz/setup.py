# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyeupi']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.23.0,<3.0.0']

entry_points = \
{'console_scripts': ['pyeupi = pyeupi:main']}

setup_kwargs = {
    'name': 'pyeupi',
    'version': '1.1',
    'description': 'Python API for the European Union anti-phishing initiative.',
    'long_description': "Client API for EUPI\n===================\n\n[![Build Status](https://travis-ci.org/Rafiot/PyEUPI.svg?branch=master)](https://travis-ci.org/Rafiot/PyEUPI)\n[![Documentation Status](https://readthedocs.org/projects/pyeupi/badge/?version=latest)](http://pyeupi.readthedocs.org/en/latest/?badge=latest)\n\nClient API to query the Phishing Initiative service.\n\nInstallation\n============\n\nFrom the repository:\n\n```\n    python setup.py install\n```\n\nOr via pip:\n\n```\n    pip install pyeupi\n```\n\nSearch queries\n==============\n\n```\n    from pyeupi import PyEUPI\n    p = PyEUPI('<Api key>')\n    p.search(content='circl')\n    p.search_url(tld='lu')\n    p.search_submissions()\n```\n",
    'author': 'Raphaël Vinot',
    'author_email': 'raphael.vinot@circl.lu',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/CIRCL/PyEUPI',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
