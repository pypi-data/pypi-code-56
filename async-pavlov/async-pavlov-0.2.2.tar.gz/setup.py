# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pavlov']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'async-pavlov',
    'version': '0.2.2',
    'description': 'Async wrapper for Pavlov VR RCON commands',
    'long_description': '# async-pavlov\nAsync wrapper for pavlov RCON commands\n\n# Requirements\nPython 3.7+\n\n# Usage\n```py\nimport asyncio\nfrom pavlov import PavlovRCON\n\nasync def main():\n    pavlov = PavlovRCON("127.0.0.1", 9104, "password")\n    data = await pavlov.send("ServerInfo")\n    print(data)\n\nasyncio.run(main())\n```',
    'author': 'makubob',
    'author_email': 'makupi@icloud.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/makupi/async-pavlov',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
