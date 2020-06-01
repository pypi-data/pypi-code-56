# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['zealous', 'zealous.rpc', 'zealous.rpc.asyncioq', 'zealous.schema']

package_data = \
{'': ['*']}

install_requires = \
['pydantic>=1.4,<2.0']

setup_kwargs = {
    'name': 'zealous',
    'version': '0.2.3',
    'description': 'Zealous Framework',
    'long_description': "# Zealous Framework\n\n[![pipeline status](https://gitlab.com/unstashed/zealous/badges/master/pipeline.svg)](https://gitlab.com/unstashed/zealous/-/commits/master)\n[![coverage report](https://gitlab.com/unstashed/zealous/badges/master/coverage.svg)](https://gitlab.com/unstashed/zealous/-/commits/master)\n\n---\n\n**Documentation:** <https://python-zealous.gitlab.io/zealous/>\n**Source Code:** <https://gitlab.com/python-zealous/zealous>\n\n---\n\nZealous is a framework that aims to simplify specification-driven development.\n\nIt is built from the ground up with emphasis on static type checking to ensure that the\nspecification is respected while developing around it.\n\nThe framework's core elements run in an asyncio event loop so concurrency is supported\nout of the box.\n",
    'author': 'Jonathan Gravel',
    'author_email': 'jo@stashed.dev',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.com/python-zealous/zealous',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
