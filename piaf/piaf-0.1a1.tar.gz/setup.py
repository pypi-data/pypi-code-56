# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['piaf', 'piaf.comm', 'piaf.examples']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'piaf',
    'version': '0.1a1',
    'description': 'A FIPA-compliant Agent Platform written in python.',
    'long_description': '# Python Intelligent Agent Framework (piaf)\n\n![pipeline status](https://gitlab.com/ornyhtorinque/piaf/badges/master/pipeline.svg)\n![coverage report](https://gitlab.com/ornyhtorinque/piaf/badges/master/coverage.svg?job=coverage)\n\n\nThe aim of piaf is to provide a FIPA-compliant agent framework using Python.\n\n**For now, this work is experimental and subject to changes.**\n\n## Documentation\nAPI documentation is available here: https://gitlab.com/ornythorinque/piaf/-/wikis/home\n\n## Author(s)\n* ornythorinque (pierredubaillay@outlook.fr)\n',
    'author': 'Pierre DUBAILLAY',
    'author_email': 'pierredubaillay@outlook.fr',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.com/ornythorinque/piaf',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
