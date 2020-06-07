# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['butterrobot',
 'butterrobot.lib',
 'butterrobot.platforms',
 'butterrobot_plugins_contrib']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.6.2,<4.0.0',
 'colorama>=0.4.3,<0.5.0',
 'quart>=0.11.3,<0.12.0',
 'structlog>=20.1.0,<21.0.0']

entry_points = \
{'butterrobot.plugins': ['dev.ping = '
                         'butterrobot_plugins_contrib.dev:PingPlugin',
                         'fun.loquito = '
                         'butterrobot_plugins_contrib.fun:LoquitoPlugin']}

setup_kwargs = {
    'name': 'butterrobot',
    'version': '0.0.2a1',
    'description': 'What is my purpose?',
    'long_description': '# Butter Robot\n\n[![Docker Repository on Quay](https://quay.io/repository/fmartingr/butterrobot/status "Docker Repository on Quay")](https://quay.io/repository/fmartingr/butterrobot)\n\nPython framework to create bots for several platforms.\n\n![Butter Robot](./assets/icon@120.png)\n\n> What is my purpose?\n\n## Supported platforms\n\n| Name            | Receive messages | Send messages |\n| --------------- | ---------------- | ------------- |\n| Slack (app)     | Yes              | Yes           |\n| Slack (webhook) | Planned          | No[^1]            |\n| Telegram        | Yes              | Yes           |\n\n[^1]: Slack webhooks only supports answering to incoming event, not\n      sending messages on demand.\n\n## Provided plugins\n\n### Butter robot\n\n- [ ] Help\n- [ ] Usage\n- [ ] Changelog\n\n### Development\n\n- [x] Ping\n\n### Fun and entertainment\n\n- [ ] Dice roll\n- [x] Loquito\n\n## Installation\n\n### PyPi\n\nYou can run it directly by installing the package and calling it\nwith `python` though this is not recommended and only intended for\ndevelopment purposes.\n\n```\n$ pip install --user butterrobot\n$ python -m butterrobot\n```\n\n### Containers\n\nThe `fmartingr/butterrobot` container image is published on quay.io to\nuse with your favourite tool:\n\n```\npodman run -d --name butterrobot -p 8080:8080 quay.io/fmartingr/butterrobot\n```\n\n## Contributing\n\nTo run the project locally you will need [poetry](https://python-poetry.org/).\n\n```\ngit clone git@github.com:fmartingr/butterrobot.git\ncd butterrobot\npoetry install\n```\n\nCreate a `.env-local` file with the required environment variables,\nyou have [an example file](.env-example).\n\n```\nSLACK_TOKEN=xxx\nTELEGRAM_TOKEN=xxx\n...\n```\n\nAnd then you can run it directly with poetry\n\nTODO: Autoload .env-local\n\n```\ndocker run -it --rm --env-file .env-local -p 5000:5000 -v $PWD/butterrobot:/etc/app/butterrobot local/butterrobot python -m butterrobot\n```\n',
    'author': 'Felipe Martin',
    'author_email': 'me@fmartingr.com',
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
