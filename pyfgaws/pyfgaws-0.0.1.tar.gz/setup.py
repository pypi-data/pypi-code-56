# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyfgaws',
 'pyfgaws.batch',
 'pyfgaws.batch.tests',
 'pyfgaws.core',
 'pyfgaws.logs',
 'pyfgaws.logs.tests',
 'pyfgaws.tests']

package_data = \
{'': ['*']}

install_requires = \
['attrs>=19.3.0,<20.0.0',
 'boto3-stubs[batch,logs]>=1.13.19,<2.0.0',
 'boto3>=1.13.18,<2.0.0',
 'botocore>=1.13.18,<2.0.0',
 'defopt>=6.0,<7.0',
 'namegenerator>=1.0.6,<2.0.0']

entry_points = \
{'console_scripts': ['fgaws-tools = pyfgaws.__main__:main']}

setup_kwargs = {
    'name': 'pyfgaws',
    'version': '0.0.1',
    'description': 'Tools and python libraries for working with AWS.',
    'long_description': '# pyfgaws\n\n# Getting Setup\n\nConda is used to install a specific version of python and [poetry](https://github.com/python\n-poetry/poetry) which is then used to manage the python development environment.  If not already\n installed, install [miniconda from the latest platform-appropriate installer](miniconda-link\n ). Then run:\n\n```\nconda create -n pyfgaws -c bioconda --file conda-requirements.txt\n```\n\nThen activate the new environment and install the toolkit:\n\n```\nconda activate pyfgaws\npoetry install\n```\n\n[miniconda-link]: https://docs.conda.io/en/latest/miniconda.html',
    'author': 'Nils Homer',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/fulcrumgenomics/pyfgaws',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
