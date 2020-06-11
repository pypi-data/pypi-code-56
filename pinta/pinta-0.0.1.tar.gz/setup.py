# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pinta', 'pinta.cli']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.2,<8.0.0', 'httpx>=0.13.3,<0.14.0', 'rich>=2.0.1,<3.0.0']

entry_points = \
{'console_scripts': ['pinta = pinta.cli.__main__:main']}

setup_kwargs = {
    'name': 'pinta',
    'version': '0.0.1',
    'description': 'Job management on GPU clusters',
    'long_description': '# Pinta: Job management on GPU clusters 🍺\n\n## Installation\n\nTo install the command-line client:\n\n``` bash\npip3 install pinta\n```\n\nTo install the backend API server:\n\n``` bash\npip3 install pinta-api\n```\n\nPinta requires Python 3.8.\n\n\n## Development\n\nTo start contributing to Pinta:\n\n``` bash\ngit clone git@github.com:qed-usc/pinta.git\ncd pinta\npoetry install\n```\n\nYou can run Pinta from the local directory with `poetry run pinta` (or by first\nstarting `poetry shell` and then `pinta`).\n\nTo run the tests: `poetry run pytest`.\n\nTo check the documentation: `poetry run mkdocs serve`.\n\nTo deploy the documentation: `poetry run mkdocs gh-deploy`.\n',
    'author': 'Pinta Team',
    'author_email': 'pinta-l@usc.edu',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://qed.usc.edu/pinta',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
