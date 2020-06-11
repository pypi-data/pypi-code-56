# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['graphql_sqlalchemy',
 'graphql_sqlalchemy.dialects',
 'graphql_sqlalchemy.dialects.pg']

package_data = \
{'': ['*']}

install_requires = \
['SQLAlchemy>=1.2,<2', 'graphql-core>=3.0.0,<4']

setup_kwargs = {
    'name': 'graphql-sqlalchemy',
    'version': '0.5.2',
    'description': 'Generate GraphQL Schemas from your SQLAlchemy models',
    'long_description': '# graphql-sqlalchemy\n\n[![PyPI version](https://badge.fury.io/py/graphql-sqlalchemy.svg)](https://badge.fury.io/py/graphql-sqlalchemy)\n[![Build Status](https://travis-ci.com/gzzo/graphql-sqlalchemy.svg?branch=master)](https://travis-ci.com/gzzo/graphql-sqlalchemy)\n[![codecov](https://codecov.io/gh/gzzo/graphql-sqlalchemy/branch/master/graph/badge.svg)](https://codecov.io/gh/gzzo/graphql-sqlalchemy)\n[![Code Style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)\n\nGenerate GraphQL Schemas from your SQLAlchemy models\n\n# Install\n```\npip install graphql-sqlalchemy\n```\n\n# Usage\n\n```python\nfrom ariadne.asgi import GraphQL\nfrom fastapi import FastAPI\nfrom graphql_sqlalchemy import build_schema\n\nfrom .session import Session\nfrom .base import Base\n\n\napp = FastAPI()\nsession = Session()\n\nschema = build_schema(Base)\n\napp.mount("/graphql", GraphQL(schema, context_value=dict(session=session)))\n```\n\n# Query\n\n```graphql\nquery MyQuery {\n    user(\n        where: {\n            _or: [\n                { id: { _gte: 5 } },\n                { name: { _like: "%bob%" } },\n            ]\n        }\n    ) {\n        id\n        name\n    }\n    model_by_pk(id: 5) {\n        createtime\n    }\n}\n```\n',
    'author': 'Guido Rainuzzo',
    'author_email': 'hi@guido.nyc',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/gzzo/graphql-sqlalchemy',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.0,<4',
}


setup(**setup_kwargs)
