# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['qwazzock']

package_data = \
{'': ['*'],
 'qwazzock': ['static/audio/*',
              'static/css/*',
              'static/dialog-polyfill/*',
              'static/icons/*',
              'static/images/*',
              'static/js/*',
              'templates/*']}

install_requires = \
['eventlet>=0.25.2,<0.26.0',
 'flask-socketio>=4.2.1,<5.0.0',
 'flask>=1.1.2,<2.0.0',
 'pyopenssl>=19.1.0,<20.0.0']

entry_points = \
{'console_scripts': ['qwazzock = qwazzock:run']}

setup_kwargs = {
    'name': 'qwazzock',
    'version': '0.11.1',
    'description': 'Qwazzock quiz app.',
    'long_description': None,
    'author': 'Dave Randall',
    'author_email': '19395688+daveygit2050@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
