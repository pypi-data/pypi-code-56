# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['slow_django']

package_data = \
{'': ['*']}

install_requires = \
['django>=3.0.7,<4.0.0']

setup_kwargs = {
    'name': 'slow-django',
    'version': '1.1.0',
    'description': 'Django, but slower',
    'long_description': "# Slow Django\n\n> Django, but slower\n\nEver thought that your project was too fast?\n\n## Install\n```\npip install slow_django\n```\n\n```python\n# settings.py\n\nimport slow_django\n\nSLOW_MIN = 2 # Minimum page load in seconds\nSLOW_MAX = 10 # Maximum-ish page load in seconds\n\nMIDDLEWARE = [\n    'django.middleware.security.SecurityMiddleware',\n    'django.contrib.sessions.middleware.SessionMiddleware',\n    'django.middleware.common.CommonMiddleware',\n    'django.middleware.csrf.CsrfViewMiddleware',\n    'django.contrib.auth.middleware.AuthenticationMiddleware',\n    'django.contrib.messages.middleware.MessageMiddleware',\n    'django.middleware.clickjacking.XFrameOptionsMiddleware',\n    'slow_django.middleware.slowdown'\n]\n```",
    'author': 'pbexe',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/pbexe/slow-django',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
