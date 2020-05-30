# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['racingbars']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'racingbars',
    'version': '0.0.0',
    'description': 'Bar chart race, easy to use, based on d3',
    'long_description': '',
    'author': 'Hatem Hosny',
    'author_email': 'hatemhosny@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
