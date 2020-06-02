# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['thqm']

package_data = \
{'': ['*'], 'thqm': ['static/*', 'static/css/*', 'static/js/*', 'templates/*']}

install_requires = \
['jinja2>=2.11.2,<3.0.0']

extras_require = \
{u'qrcode': ['pyqrcode>=1.2.1,<2.0.0']}

entry_points = \
{'console_scripts': ['thqm = thqm.__cli__:main']}

setup_kwargs = {
    'name': 'thqm',
    'version': '1.1.2',
    'description': 'remote command execution made easy.',
    'long_description': '<h1 align="center">thqm</h1>\n<h3 align="center"><img src="https://i.imgur.com/gVB270Z.png" width="150"></h3>\n<h5 align="center">Remote command execution made easy.</h5>\n\n<p align="center">\n  <a href="https://github.com/loiccoyle/thqm/actions?query=workflow%3Atests"><img src="https://github.com/loiccoyle/thqm/workflows/tests/badge.svg"></a>\n  <a href="https://pypi.org/project/thqm/"><img src="https://img.shields.io/pypi/v/thqm"></a>\n  <a href="./LICENSE.md"><img src="https://img.shields.io/badge/license-MIT-blue.svg"></a>\n  <img src="https://img.shields.io/badge/platform-linux%20%7C%20macOS%20%7C%20windows-informational">\n</p>\n<img src="https://i.imgur.com/OrK36nl.png?1" align=\'right\' width=\'170px\'>\n\n> `thqm` takes its name from the arabic \xd8\xaa\xd8\xad\xd9\x83\xd9\x85, pronounced tahakum, meaning control.\n\n`thqm` makes it very easy to setup a simple remote control interface on the host machine.\n\n`thqm` is a nifty little HTTP server which reads from standard input. It dynamically generates a simple button menu based on the provided `stdin` and outputs any button the user presses to `stdout`.\nIn a sense its kind of like the [`dmenu`](https://tools.suckless.org/dmenu/)/[`rofi`](https://github.com/davatorium/rofi) of HTTP servers.\n\nThis makes it very flexible and script friendly. See the [examples](./examples) folder for some scripts.\n\n&nbsp;\n\n&nbsp;\n\n# Installation\n```shell\npip install thqm\n```\n`thqm` should work on linux, MacOS and Windows.\n\nIt usually is a good idea to use a virtual environment, or maybe consider using [pipx](https://github.com/pipxproject/pipx).\n\n# Dependencies\n`thqm` requires the following to run:\n  * `python3`\n  * `jinja`\n\nOptional:\n  * `pyqrcode` for qrcode generation.\n\n# Usage\nCheck the [examples](./examples) folder for some usage examples.\n\n```\n$thqm --help\n\nusage: thqm [-h] [-p PORT] [-q] [-pw PASSWORD] [-u USERNAME] [-s SEPERATOR]\n            [-o]\n\nRemote command execution made easy.\n\noptional arguments:\n  -h, --help            show this help message and exit\n  -p PORT, --port PORT  Port number. (default: 8888)\n  -q, --qrcode          Show the qrcode and exits, requires "pyqrcode".\n                        (default: False)\n  -pw PASSWORD, --password PASSWORD\n                        Authentication password. (default: None)\n  -u USERNAME, --username USERNAME\n                        Authentication username, only used if a PASSWORD is\n                        provided. (default: thqm)\n  -s SEPERATOR, --seperator SEPERATOR\n                        Entry seperator pattern. (default: )\n  -o, --oneshot         Shutdown server after first click. (default: False)\n```\nUse the `-u` and `-pw` arguments to set a username and password to restrict access. The authentication is handled with [HTTP basic authentication](https://en.wikipedia.org/wiki/Basic_access_authentication).\n\nWith the `-s` argument you can define the pattern on which to split `stdin`.\n\nThe `-o` flag will stop the server after the first button press.\n\nThe `-q` (requires `pyqrcode`) flag will print a qr-code in the terminal, this qr-code contains the credentials so it will bypass any authentication, the same is true for the in browser qr-code. This makes it particularly easy to share access with others.\n\n# TODO\n- [ ] remove external css/JS dependencies\n- [ ] allow for custom `index.html` template and `index.css`\n',
    'author': 'Loic Coyle',
    'author_email': 'loic.coyle@hotmail.fr',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/loiccoyle/thqm',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
