# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['django_icons', 'django_icons.renderers', 'django_icons.templatetags']

package_data = \
{'': ['*']}

install_requires = \
['django>=2.2,<4.0']

setup_kwargs = {
    'name': 'django-icons',
    'version': '2.0.0',
    'description': 'Icons for Django',
    'long_description': 'django-icons\n------------\n\nIcons for Django\n\n.. image:: https://travis-ci.org/zostera/django-icons.svg?branch=master\n    :target: https://travis-ci.org/zostera/django-icons\n\n.. image:: https://coveralls.io/repos/github/zostera/django-icons/badge.svg?branch=develop\n   :target: https://coveralls.io/github/zostera/django-icons?branch=develop\n\n.. image:: https://img.shields.io/pypi/v/django-icons.svg\n    :target: https://pypi.python.org/pypi/django-icons\n    :alt: Latest PyPI version\n\n.. image:: https://img.shields.io/badge/code%20style-black-000000.svg\n    :target: https://github.com/ambv/black\n\nFeatures\n========\n\nUse simple template tags to generate icons in your web application.\nSupports *Font Awesome* out of the box, easily adaptable for other icon libraries.\n\nThe basic usage in a Django template::\n\n   {% load icons %}\n   {% icon \'edit\' %}\n\n\nRequirements\n============\n\nThis package requires a Python 3.6 or newer and Django 2.2 or newer.\n\nThe combination must be supported by the Django Project. See "Supported Versions" on https://www.djangoproject.com/download/.\n\nRunning the demo\n================\n\nYou can run the small demo app that is part of the test suite.\nThis requires Django, so you may have to `pip install django` in your environment.\nTo run the demo, from the root of the project (where you can find `manage.py`, run::\n\n   python manage.py runserver\n\n\nRunning the tests\n=================\n\nThe test suite uses `tox`. Run the complete test suite like this::\n\n   tox\n\nRun the tests only for the current environment like this::\n\n   python manage.py test\n\n\nOrigin\n======\n\nOur plans at Zostera for an icon tool originate in https://github.com/dyve/django-bootstrap3.\nWe isolated this into a Font Awesome tool in https://github.com/zostera/django-fa.\nWhen using our own product, we felt that the icon tool provided little improvement over plain HTML.\nAlso, Font Awesome\'s icon names did not match the the intended function of the icon. This is how we came\nto think of a library that\n\n- Took a limited number of arguments\n- Converted those arguments into an icon\n- Was able to support multiple icon libraries\n- And could easily be extended by users\n\nThis is how we came to write and use `django-icons`.\n',
    'author': 'Dylan Verheul',
    'author_email': 'dylan@zostera.nl',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/zostera/django-icons',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
