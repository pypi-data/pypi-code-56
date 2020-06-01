# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['bootstrap4', 'bootstrap4.templatetags']

package_data = \
{'': ['*'],
 'bootstrap4': ['templates/bootstrap4/*', 'templates/bootstrap4/widgets/*']}

install_requires = \
['beautifulsoup4>=4.9.1,<5.0.0', 'django>=2.2,<4.0']

setup_kwargs = {
    'name': 'django-bootstrap4',
    'version': '2.0.0',
    'description': 'Bootstrap support for Django projects',
    'long_description': '======================\nBootstrap 4 for Django\n======================\n\n.. image:: https://travis-ci.org/zostera/django-bootstrap4.svg?branch=develop\n    :target: https://travis-ci.org/zostera/django-bootstrap4\n\n.. image:: https://img.shields.io/coveralls/zostera/django-bootstrap4/master.svg\n    :target: https://coveralls.io/r/zostera/django-bootstrap4?branch=master\n\n.. image:: https://img.shields.io/pypi/v/django-bootstrap4.svg\n    :target: https://pypi.python.org/pypi/django-bootstrap4\n    :alt: Latest PyPI version\n\n.. image:: https://img.shields.io/badge/code%20style-black-000000.svg\n    :target: https://github.com/ambv/black\n\nBootstrap 4 integration for Django.\n\n\nGoal\n----\n\nThe goal of this project is to seamlessly blend Django and Bootstrap 4.\n\n\nRequirements\n------------\n\n- Django >= 2.1 (and `compatible Python versions <https://docs.djangoproject.com/en/2.2/faq/install/#what-python-version-can-i-use-with-django>`_)\n\n\nDocumentation\n-------------\n\nThe full documentation is at https://django-bootstrap4.readthedocs.io/\n\n\nInstallation\n------------\n\n1. Install using pip:\n\n   ``pip install django-bootstrap4``\n\n   Alternatively, you can install download or clone this repo and call ``pip install -e .``.\n\n2. Add to ``INSTALLED_APPS`` in your ``settings.py``:\n\n   ``\'bootstrap4\',``\n\n3. In your templates, load the ``bootstrap4`` library and use the ``bootstrap_*`` tags:\n\n\nExample template\n----------------\n\n   .. code:: Django\n\n    {% load bootstrap4 %}\n\n    {# Display a form #}\n\n    <form action="/url/to/submit/" method="post" class="form">\n        {% csrf_token %}\n        {% bootstrap_form form %}\n        {% buttons %}\n            <button type="submit" class="btn btn-primary">Submit</button>\n        {% endbuttons %}\n    </form>\n\n\nDemo\n----\n\nA demo app is provided in `demo`. You can run it from your virtualenv with `python manage.py runserver`.\n\n\nBugs and suggestions\n--------------------\n\nIf you have found a bug or if you have a request for additional functionality, please use the issue tracker on GitHub.\n\nhttps://github.com/zostera/django-bootstrap4/issues\n\n\nLicense\n-------\n\nYou can use this under BSD-3-Clause. See `LICENSE\n<LICENSE>`_ file for details.\n\n\nAuthor\n------\n\nDeveloped and maintained by `Zostera <https://zostera.nl/>`_.\n\nOriginal author & Development lead: `Dylan Verheul <https://github.com/dyve>`_.\n\nThanks to everybody that has contributed pull requests, ideas, issues, comments and kind words.\n\nPlease see AUTHORS.rst for a list of contributors.\n',
    'author': 'Dylan Verheul',
    'author_email': 'dylan@zostera.nl',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/zostera/django-bootstrap4',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
