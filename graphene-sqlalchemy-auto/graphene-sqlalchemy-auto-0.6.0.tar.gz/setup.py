# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['graphene_sqlalchemy_auto']

package_data = \
{'': ['*']}

install_requires = \
['graphene-sqlalchemy<2.3.0']

setup_kwargs = {
    'name': 'graphene-sqlalchemy-auto',
    'version': '0.6.0',
    'description': 'generate default graphene schema from sqlalchemy model base on [graphene-sqlalchemy](https://github.com/graphql-python/graphene-sqlalchemy.git)\n',
    'long_description': 'generate default graphene schema from sqlalchemy model base on [graphene-sqlalchemy](https://github.com/graphql-python/graphene-sqlalchemy.git)\n\n# Installation\n\njust run\n```shell script\npip install graphene_sqlalchemy_auto\n```\n# Features\n\n- auto add `offset` `limit` `totalCount` to pagination\n- auto add `dbId` for model\'s database id\n- mutation auto return ok for success,message for more information and output for model data\n\n\n# How To Use\nexample :\n```python\nfrom graphene_sqlalchemy_auto import QueryObjectType,MutationObjectType\nfrom sqlalchemy.ext.declarative import declarative_base\nimport graphene\nfrom sqlalchemy.orm import sessionmaker\n\nBase = declarative_base() \nSession = sessionmaker()\n\nclass Query(QueryObjectType):\n    class Meta:\n        declarative_base = Base\n        exclude_models = ["User"] # exclude models\n\nclass Mutation(MutationObjectType):\n    class Meta:\n        declarative_base = Base\n        session=Session() # mutate used\n        \n        include_object = []# you can use yourself mutation UserCreateMutation, UserUpdateMutation\n\n\nschema = graphene.Schema(query=Query, mutation=Mutation)\n\n```\n\nabout many-to-many mutation\n\n>now you can use schema everywhere.some like flask,fastapi\n\n>also more example you can find in [example](https://github.com/goodking-bq/graphene-sqlalchemy-auto/tree/master/example)',
    'author': 'golden',
    'author_email': 'goodking_bq@hotmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/goodking-bq/graphene-sqlalchemy-auto',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
