# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['opennem',
 'opennem.agent',
 'opennem.commands',
 'opennem.datetimes',
 'opennem.db',
 'opennem.db.migrations',
 'opennem.db.migrations.versions',
 'opennem.db.models',
 'opennem.nem_derived',
 'opennem.pipelines',
 'opennem.schema',
 'opennem.settings',
 'opennem.spiders',
 'opennem.spiders.nem',
 'opennem.utils']

package_data = \
{'': ['*']}

install_requires = \
['alembic>=1.4.2,<2.0.0',
 'click>=7.1.2,<8.0.0',
 'pydantic>=1.5.1,<2.0.0',
 'python-dotenv>=0.13.0,<0.14.0',
 'pyyaml>=5.3.1,<6.0.0',
 'requests>=2.23.0,<3.0.0',
 'scrapy>=2.1.0,<3.0.0',
 'sentry-sdk>=0.14.4,<0.15.0',
 'smart_open>=2.0.0,<3.0.0',
 'sqlalchemy>=1.3.17,<2.0.0']

entry_points = \
{'console_scripts': ['bluestoned = opennem.cli:main']}

setup_kwargs = {
    'name': 'opennem',
    'version': '0.2.0',
    'description': 'opennem engine agent',
    'long_description': None,
    'author': 'Dylan McConnell',
    'author_email': 'dylan.mcconnell@unimelb.edu.au',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
