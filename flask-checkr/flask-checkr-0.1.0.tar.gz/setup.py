# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['flask_checkr']

package_data = \
{'': ['*']}

install_requires = \
['flask>=1.1.2,<2.0.0', 'jsonschema>=3.2.0,<4.0.0']

setup_kwargs = {
    'name': 'flask-checkr',
    'version': '0.1.0',
    'description': 'Easily validate Flask requests with JSONSchema.',
    'long_description': '.. _Postman: https://www.getpostman.com/\n.. _Flask: http://flask.pocoo.org/\n\n=============\nFlask-Checkr\n=============\n\nA tool that allows for quick and extensible JSON Schema validation for a Flask_ application.\n\n',
    'author': 'Pavel P.',
    'author_email': 'pascaripavel@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/pavelpascari/flask-checkr',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=2.7,<3.0',
}


setup(**setup_kwargs)
