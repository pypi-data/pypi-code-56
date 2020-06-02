# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['Playwright']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'robotframework-playwright',
    'version': '0.1.0',
    'description': '',
    'long_description': '# robotframework-playwright\n\nRobot Framework Playwright library\n\n# Development\n\n- https://www.python.org/downloads/\n- `python -m pip install poetry`\n- https://nodejs.org/\n- https://classic.yarnpkg.com/en/docs/install\n\nInstall `yarn install` and `poetry install`.\n\nRun robot framework tests `poetry run robot atest`.\nRun pytests `poetry run pytest`.\n',
    'author': 'Mikko Korpela',
    'author_email': 'mikko.korpela@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/mkorpela/robotframework-playwright',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
