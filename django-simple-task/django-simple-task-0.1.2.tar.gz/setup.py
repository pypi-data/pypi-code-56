# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['django_simple_task']

package_data = \
{'': ['*']}

install_requires = \
['asgiref>=3.2.3,<4.0.0']

setup_kwargs = {
    'name': 'django-simple-task',
    'version': '0.1.2',
    'description': 'Task runner for Django 3 without requiring other services',
    'long_description': '# Django Simple Task\n[![Github Actions](https://github.com/ericls/django-simple-task/workflows/Build/badge.svg)](https://github.com/ericls/django-simple-task/actions)\n[![Documentation Status](https://readthedocs.org/projects/django-simple-task/badge/?version=latest)](https://django-simple-task.readthedocs.io/?badge=latest)\n[![Code Coverage](https://codecov.io/gh/ericls/django-simple-task/branch/master/graph/badge.svg)](https://codecov.io/gh/ericls/django-simple-task)\n[![Python Version](https://img.shields.io/pypi/pyversions/django-simple-task.svg)](https://pypi.org/project/django-simple-task/)\n[![PyPI Package](https://img.shields.io/pypi/v/django-simple-task.svg)](https://pypi.org/project/django-simple-task/)\n[![License](https://img.shields.io/pypi/l/django-simple-task.svg)](https://github.com/ericls/django-simple-task/blob/master/LICENSE)\n\n`django-simple-task` runs background tasks in Django 3 without requiring other services and workers. It runs them in the same event loop as your ASGI application. It is not resilient as a proper task runner such as Celery, but works for some simple tasks and has less overall overheads.\n\n## Guide\n\nInstall the package:\n```bash\npip install django-simple-task\n```\n\nAdded it to installed apps:\n```python\n# settings.py\nINSTALLED_APPS = [\n\t...\n\t\'django_simple_task\'\n]\n```\nApply ASGI middleware :\n```python\n# asgi.py\nfrom django_simple_task import django_simple_task_middlware\napplication = django_simple_task_middlware(application)\n```\n\nCall a background task in Django view:\n```python\nfrom django_simple_task import defer\n\ndef task1():\n\ttime.sleep(1)\n\tprint("task1 done")\n\nasync def task2():\n\tawait asyncio.sleep(1)\n\tprint("task2 done")\n\ndef view(requests):\n\tdefer(task1)\n\tdefer(task2)\n\treturn HttpResponse(b"My View")\n```\n\nIt is required to run Django with ASGI server. [Official Doc](https://docs.djangoproject.com/en/3.0/howto/deployment/asgi/)\n\n## Configurations\n\nConcurrency level can be controlled by adding `DJANGO_SIMPLE_TASK_WORKERS` to settings. Defaults to `1`.',
    'author': 'Shen Li',
    'author_email': 'dustet@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ericls/django-simple-task',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4',
}


setup(**setup_kwargs)
