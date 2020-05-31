# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pygeojson']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'pygeojson',
    'version': '0.2.0',
    'description': 'GeoJSON library for Python with types',
    'long_description': '# pygeojson 🗺\n\nGeoJSON library for Python with [types](https://docs.python.org/3/library/typing.html).\n\nThe world doesn\'t need another\n[GeoJSON library for python](https://github.com/jazzband/geojson), but it needs\na better one. The goal of this library is to provide a simple and typed data\nmodel for GeoJSON such that y\'all can get static code check and editor support\nwith [mypy](http://mypy-lang.org/). And of course, data should be data, so the\ndata model is not polluted with inheritance, custom methods, utilities,\nextension or other "conveniences". Lastly, your data will be immutable!\n\n`pygeojson` is built on top of\n[`dataclasses`](https://docs.python.org/3/library/dataclasses.html) to provide\ntypes, immutability and default value support. Models does not inherit from one\nbut instead we use\n[`Union` types](https://docs.python.org/3/library/typing.html#typing.Union)\nwhere applicable.\n\nIn addition, `pygeojson` comes with serialization and deserialization support\nvia the `dump`, `dumps`, `load` and `loads` functions.\n\n## Installation\n\n`pygeojson` requires Python 3.7 and up. Install it via `pipenv`:\n\n```sh\npipenv install pygeojson\n```\n\nor `pip`:\n\n```sh\npip install pygeojson\n```\n\n## Usage\n\nTBD\n\n## Data model\n\nTBA\n',
    'author': 'Håkon Åmdal',
    'author_email': 'hakon@aamdal.com',
    'maintainer': 'Håkon Åmdal',
    'maintainer_email': 'hakon@aamdal.com',
    'url': 'https://github.com/hawkaa/pygeojson',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
