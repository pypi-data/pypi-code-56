# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['locuplot', 'locuplot.dto', 'locuplot.helpers', 'locuplot.locust']

package_data = \
{'': ['*'], 'locuplot': ['templates/*']}

install_requires = \
['jinja2>=2.11.2,<3.0.0',
 'logzero>=1.5.0,<2.0.0',
 'matplotlib>=3.2.1,<4.0.0',
 'mpld3>=0.3,<0.4',
 'numpy>=1.18.5,<2.0.0',
 'pandas>=1.0.4,<2.0.0']

entry_points = \
{'console_scripts': ['locuplot = locuplot.main:main']}

setup_kwargs = {
    'name': 'locuplot',
    'version': '0.1.2',
    'description': 'Python application for generating plot from locust statistics csv',
    'long_description': '# Locuplot\n\nLocuplot is a python application to generate graph based on locust statistics reporting.\n\n## Usage\nTODO: When we will release locuplot to the pip registry, complete this section.\nTODO: Reference how to install the application.\nTODO: Reference command line arguments\n\n### Install\nLocuplot is available on pypi registry, you can:\n```bash\npip install locuplot\n```\n\n### Usage\n\nThere is a help command `locuplot -h`\n\nTo use this project, there is 3 arguments to give.\n`locuplot -d example\\stats -p sample -e dist`\n\nArguments list:\n- -d | --directory => Specify the folder where the locust stats are.\n- -p | --prefix    => The prefix you gave to locust for generated stats\n- -e | --export    => The export directory you want png and html generated files (default to `./dist`)\n\n## Local setup\n\nMake sure to install [poetry](https://python-poetry.org/) first. Then, make a `poetry install` in the project\nroot directory. \n\nTo execute locuplot locally, use this commands:\n```bash\npoetry run locuplot -d example\\stats -p sample\n```\n\nFor further information you can display the helper like this:\n\n```bash\npoetry run locuplot -h\n```\n\n### Commands\n\nThese custom commands are launched via poetry and an awesome plugin named\n[taskipy](https://github.com/illBeRoy/taskipy). Go check out this project !\n\nNon exhaustive custom commands:\n\n| Command                 | Description                                     |\n|-------------------------|-------------------------------------------------|\n| poetry run task locust  | Run sample locust test                          |\n| poetry run task jupyter | Launch jupyter notebook with example statistics |\n\n',
    'author': 'pawndev',
    'author_email': 'coquelet.c@gmail.com',
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
