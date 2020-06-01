# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pymongo_inmemory']

package_data = \
{'': ['*']}

install_requires = \
['pymongo']

setup_kwargs = {
    'name': 'pymongo-inmemory',
    'version': '0.1.3',
    'description': 'A mongo mocking library with an ephemeral MongoDB running in memory.',
    'long_description': "[![PyPI version](https://badge.fury.io/py/pymongo-inmemory.svg)](https://badge.fury.io/py/pymongo-inmemory)\n\n# pymongo_inmemory\nA mongo mocking library with an ephemeral MongoDB running in memory.\n\n## Installation\n```bash\npip install pymongo-inmemory\n```\n\n## Usage\nInsert a new section to your project's `setup.cfg` for the operating system and\nmongo version you want to spin up:\n```ini\n[pymongo_inmemory]\nmongo_version = 4.0\noperating_system = osx\n```\n\nthen use the `pymongo_inmemory` client instead of original one:\n```python\nfrom pymongo_inmemory import MongoClient\n\nclient = MongoClient()  # No need to provide host\ndb = client['testdb']\ncollection = db['test-collection']\n# etc., etc.\nclient.close()\n\n# Also usable with context manager\nwith MongoClient() as client:\n    # do stuff\n```\n\n## Development\nProject is set up to develop with [poetry](https://python-poetry.org/).\n\nAfter installing Pipenv and cloning the repo, create the shell and install all\npackage requirements:\n\n```bash\n$> poetry install\n$> poetry shell\n```\n\nRun the tests:\n```bash\n$> pytest\n```\n\nIf on NIX systems you can run further tests:\n```bash\n$> bash tests/integrity/test_integrity.sh\n```\n\n**See how you can wet your feet,** check out [good first issues](https://github.com/kaizendorks/pymongo_inmemory/contribute).\n",
    'author': 'Kaizen Dorks',
    'author_email': 'kaizendorks@gmail.com',
    'maintainer': 'Ertugrul Karademir',
    'maintainer_email': 'ekarademir@gmail.com',
    'url': 'https://github.com/kaizendorks/pymongo_inmemory',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.4,<4.0',
}


setup(**setup_kwargs)
