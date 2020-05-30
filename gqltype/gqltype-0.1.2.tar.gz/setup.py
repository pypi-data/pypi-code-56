# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gqltype',
 'gqltype.contrib',
 'gqltype.contrib.aiohttp',
 'gqltype.contrib.connection',
 'gqltype.contrib.starlette',
 'gqltype.graphql_types',
 'gqltype.transform',
 'gqltype.utils']

package_data = \
{'': ['*']}

install_requires = \
['aniso8601', 'graphql-core>=3.0']

setup_kwargs = {
    'name': 'gqltype',
    'version': '0.1.2',
    'description': 'Simple way to define GraphQL schema',
    'long_description': '## Description\n\nCurrently EXPERIMENTAL.\n\n`gqltype` is a GraphQL schema generator from python type annotations.\n\n\n## Features\n\n- simple definition of GraphQL schema via python type annotations\n- builds schema based on `graphql-core>=3.0` library\n- asgi friendly\n\n\n## Installation\n\nUsing `pip`\n```bash\n$ pip install gqltype\n```\n\nUsing `poetry`\n```bash\n$ poetry add gqltype\n```\n\n\n## Quick intro\n\nLet\'s say we want to model the schema mentioned at the beginning of https://graphql.org/learn/schema/ tutorial.\n\n```python\nfrom dataclasses import dataclass\nfrom enum import Enum\nfrom typing import List\n\nimport gqltype\n\n\nclass Episode(Enum):\n    """Codename for the episodes"""\n    NEWHOPE = "new hope"\n    EMPIRE = "empire"\n    JEDI = "jedi"\n\n\n@dataclass\nclass Character:\n    """An individual person within the Star Wars universe"""\n    name: str\n    appears_in: List[Episode]\n\n\nclass LengthUnit(Enum):\n    """Measure of length"""\n    METER = "meter"\n    INCH = "inch"\n\n\n@dataclass\nclass Starship:\n    """A single transport craft that has hyperdrive capability"""\n    id: str\n    name: str\n    length: float\n\n    def resolve_length(self, unit: LengthUnit = LengthUnit.METER) -> float:\n        if unit == LengthUnit.INCH:\n            return self.length / 0.0254\n        return self.length\n\n\ndef get_character() -> Character:\n    return Character(name="R2D2", appears_in=[Episode.JEDI, Episode.NEWHOPE])\n\n\nasync def get_starship() -> Starship:\n    return Starship(id="F1000", name="Millennium Falcon", length=34.75)\n\n\ndef add_character(name: str, appears_in: List[Episode]) -> Character:\n    return Character(name=name, appears_in=appears_in)\n\n\nschema = gqltype.Schema(\n    queries=[get_character, get_starship],\n    mutations=[add_character]\n)\n\nfrom graphql.utilities import print_schema\nprint(print_schema(schema.build()))\n```\n\nIt\'ll produce the following output\n```graphql\ntype Query {\n  getCharacter: Character!\n  getStarship: Starship!\n}\n\n"""An individual person within the Star Wars universe"""\ntype Character {\n  appearsIn: [Episode!]!\n  name: String!\n}\n\n"""Codename for the episodes"""\nenum Episode {\n  NEWHOPE\n  EMPIRE\n  JEDI\n}\n\n"""A single transport craft that has hyperdrive capability"""\ntype Starship {\n  length(unit: LengthUnit! = METER): Float!\n  id: ID!\n  name: String!\n}\n\n"""Measure of length"""\nenum LengthUnit {\n  METER\n  INCH\n}\n\ntype Mutation {\n  addCharacter(name: String!, appearsIn: [Episode!]!): Character!\n}\n```\n\nIn order to run server with this schema we can use Starlette\n```python\nif __name__ == "__main__":\n    import uvicorn\n    from gqltype.contrib.starlette import GraphQLApp\n    from starlette.applications import Starlette\n    from starlette.routing import Route\n\n    app = Starlette(routes=[Route("/graphql", GraphQLApp(schema=schema))])\n    uvicorn.run(app)\n```\n\nExecuting\n```graphql\n{\n  getCharacter {\n    name\n    appearsIn\n  }\n\n  getStarship {\n    id\n    name\n    length(unit: INCH)\n  }\n}\n```\ngives\n```json\n{\n  "data": {\n    "getCharacter": {\n      "name": "R2D2",\n      "appearsIn": [\n        "JEDI",\n        "NEWHOPE"\n      ]\n    },\n    "getStarship": {\n      "id": "F1000",\n      "name": "Millennium Falcon",\n      "length": 1368.1102362204724\n    }\n  }\n}\n```\n\n## TODO\n\n- sanity checks\n    - warn if class and resolve method specify different types\n\n- generic resolvers for certain types?\n\n- gqltype.F ? -- field definition\n\n- core part and high level part\n\n- business level\n    - validation for input values\n    - serialization of output values\n',
    'author': 'miphreal',
    'author_email': 'miphreal@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/miphreal/gqltype',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<3.9',
}


setup(**setup_kwargs)
