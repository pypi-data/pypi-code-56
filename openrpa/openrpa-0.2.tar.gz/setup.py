# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['openrpa']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'openrpa',
    'version': '0.2',
    'description': '',
    'long_description': '# pypi-project-template\n\n## Minimal steps to create new PyPi project\n\n1. create folder structure / clone this project\n2. edit *PROJECT_NAME* in `pyproject.toml` and rename folder `PROJECT_NAME` to match\n3. edit *AUTHOR_EMAIL* and *AUTHOR_FULLNAME* ("firstname lastname") in `pyproject.toml`\n4. edit *VERSION_NUMBER* in `pyproject.toml` and `__init__.py` to match (eg. "0.1.0")\n5. edit `README.md`, this represents README on project homepage in PyPi\n6. (OPTIONAL) edit `pyproject.toml` dependencies, license and other specifics if needed\n7. `poetry build`\n8. `poetry publish -u PYPI_USERNAME -p PYPI_PASSWORD`\n\nAfter project has been created all information about the project can be changed.\n\nExtra information: https://johnfraney.ca/posts/2019/05/28/create-publish-python-package-poetry/',
    'author': 'Orlof',
    'author_email': 'orlof@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
