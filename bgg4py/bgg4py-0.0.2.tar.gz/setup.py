# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bgg4py', 'bgg4py.valueobject']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.2,<8.0.0',
 'devtools>=0.5.1,<0.6.0',
 'pydantic>=1.5.1,<2.0.0',
 'requests>=2.23.0,<3.0.0',
 'xmltodict>=0.12.0,<0.13.0']

setup_kwargs = {
    'name': 'bgg4py',
    'version': '0.0.2',
    'description': '',
    'long_description': '# bgg4py\n\nbgg4py is a Boardgamegeek API wrapper.\n\n<a href="https://pypi.org/project/bgg4py" target="_blank">\n    <img src="https://badge.fury.io/py/bgg4py.svg" alt="Package version">\n</a>\n\n## Requirements\n\nPython 3.7+\n\n## Installation\n\n```console\n$ pip install bgg4py\n```\n\n## Example\n\n### CLI\n\n* Check Command Options\n```\n$ python -m bgg4py.cli\nUsage: cli.py [OPTIONS] COMMAND [ARGS]...\n\nOptions:\n  --help  Show this message and exit.\n\nCommands:\n  family-items\n  forum-lists\n  forums\n  geeklist\n  hot-items\n  search\n  thing\n  threads\n  user-collection\n  users\n\n```\n\n* Check Subcommand Options\n```\n$ python -m bgg4py.cli users\nUsage: cli.py users [OPTIONS]\nTry \'cli.py users --help\' for help.\n\nError: Missing option \'--name\'.\n```\n\n* Run!\n```\n$ python -m bgg4py.cli users --name hiroaqii\n\nhttps://www.boardgamegeek.com/xmlapi2/user?name=hiroaqii&guilds=1&hot=1&top=1\n\n{\n    "id": 1422482,\n    "name": "hiroaqii",\n    "firstname": "hiro",\n    "lastname": "aqii",\n    "avatarlink": "N/A",\n    "yearregistered": 2016,\n    "lastlogin": "2020-06-06",\n    "stateorprovince": "",\n    "country": "",\n    "webaddress": "",\n    "xboxaccount": "",\n    "wiiaccount": "",\n    "psnaccount": "",\n    "battlenetaccount": "",\n    "steamaccount": "",\n    "traderating": 0,\n    "marketrating": 1\n}\n```\n\n### Script\n\n```Python\nfrom bgg4py import api\n\nret = api.user_collection(\'hiroaqii\')\n\n# returns a dictionary representing the model as JSON Schem\nprint(ret.schema())\n\n# output example\nprint(ret.item_list[0].image)\nprint(retret.item_list[0])\nprint(ret.item_list[0].status)\nprint(ret.item_list[0].status.lastmodified)\nprint("\\n".join([item.name for item in ret.item_list]))\n\n# output json\nret_json = json.dumps(ret.dict(), indent=4, ensure_ascii=False)\npritn(ret_json)\n\n\n```',
    'author': 'hiroaqii',
    'author_email': 'hiroaqii@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/hiroaqii/bgg4py',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
