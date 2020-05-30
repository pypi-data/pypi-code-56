# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['clint', 'clint.packages', 'clint.packages.colorama', 'clint.textui']

package_data = \
{'': ['*']}

modules = \
['functions', 'core', 'readme']
entry_points = \
{'console_scripts': ['gossip = core:app']}

setup_kwargs = {
    'name': 'dev-gossip',
    'version': '0.2.9',
    'description': '',
    'long_description': " **devGossip**\n-------------------------------------------\n#### **overview**\n        devGossip is a platform where employees and the likes come to blow of some steam and get the latest\n        gists. with gossips ranging from underpaying bosses to gossips of the history of the nagasaki\n        and hiroshima bombings. at devGossip, You can get it all.\n        Please Note, we pride ourselves in keeping your identity secret and as such,\n        do not ask for any private information from you.\n        so what are you waiting for, follow the instructions below and let's get you signed up.\n\n- ##### Setting it up from your command line\n\n    - step 1 `pip install dev-gossip`\n    - step 2 press `gossip`\n\n- ##### Features\n\n    - A user can register with no two users able to have the same username\n    - Full disclosure and security is promised as no sensitive information is collected nor stored\n    - Posts (usually called a gossip) can be made by a user\n    - Other users posts can be viewed in the order of latest post\n    - A user can safely delete his post when he so desires\n    - Gossip Threads Can be Formed when A user comments on Another Users Post(Gossip)\n    - All gossips have a unique element called a gossipTag which can be used to fetch any particular\n    gossip at any given time\n    - great user friendly interface with helpful instructions and soothing\n     colors that will blow you away. The display is simply breathtaking. \n    - A user can wow and unwow a post \n ",
    'author': 'shols232',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'py_modules': modules,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
