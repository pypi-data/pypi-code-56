# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['randalgo1']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['randalgo = randalgo1:app']}

setup_kwargs = {
    'name': 'randalgo1',
    'version': '0.1.8',
    'description': 'a console app that fetches random question from public api',
    'long_description': '# RANDALGO \nA console app that returns random question with the use of <a href="https://opentdb.com/api_config.php">Open trivia database API</a>\n\n## Requirements\nMake sure to have python installed on your system\n\nMake sure you have a strong internet connection\n## How to use the app\n<ul>\n<li>Open your console</li>\n<br>\n<li>Type "pip install randalgo1" and hit enter</li>\n<br>\n<li>Type "randalgo" and hit enter</li>\n</ul>',
    'author': 'charles',
    'author_email': 'charlesclinton2003@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.0,<4.0',
}


setup(**setup_kwargs)
