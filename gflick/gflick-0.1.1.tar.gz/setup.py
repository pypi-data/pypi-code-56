# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['gflick']

package_data = \
{'': ['*']}

install_requires = \
['httpx>=0.13.3,<0.14.0',
 'starlette>=0.13.4,<0.14.0',
 'uvicorn>=0.11.5,<0.12.0']

entry_points = \
{'console_scripts': ['gflick = gflick:prod',
                     'gflick-dev = gflick:dev',
                     'gflick-google = gflick:google']}

setup_kwargs = {
    'name': 'gflick',
    'version': '0.1.1',
    'description': '',
    'long_description': None,
    'author': 'Bùi Thành Nhân',
    'author_email': 'hi@imnhan.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
