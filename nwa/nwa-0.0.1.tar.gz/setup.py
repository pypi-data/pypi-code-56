# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nwa', 'nwa.cli.commands']

package_data = \
{'': ['*'], 'nwa': ['cli/*']}

install_requires = \
['aiodns>=2.0,<3.0',
 'aiohttp>=3.6,<4.0',
 'asyncio>=3.4,<4.0',
 'matplotlib>=3.1,<4.0',
 'networkx>=2.4,<3.0',
 'pyyaml>=5.3,<6.0']

entry_points = \
{'console_scripts': ['nwa = nwa.cli.__main__:main']}

setup_kwargs = {
    'name': 'nwa',
    'version': '0.0.1',
    'description': 'A collection of network analyses',
    'long_description': "[![github latest release](https://badgen.net/github/release/nichelia/nwa?icon=github)](https://github.com/nichelia/nwa/releases/latest/)\n[![pypi latest package](https://badgen.net/pypi/v/nwa?label=pypi%20pacakge)](https://pypi.org/project/nwa/)\n[![docker latest image](https://img.shields.io/docker/v/nichelia/nwa?label=image&logo=docker&logoColor=white)](https://hub.docker.com/repository/docker/nichelia/nwa)\n[![project license](https://badgen.net/github/license/nichelia/nwa?color=purple)](https://github.com/nichelia/nwa/blob/master/LICENSE)\n\n![nwa CI](https://github.com/nichelia/nwa/workflows/nwa%20CI/badge.svg)\n![nwa CD](https://github.com/nichelia/nwa/workflows/nwa%20CD/badge.svg)\n[![security scan](https://badgen.net/dependabot/nichelia/nwa/?label=security%20scan)](https://github.com/nichelia/nwa/labels/security%20patch)\n[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen)](https://github.com/pre-commit/pre-commit)\n\n\n[![code coverage](https://badgen.net/codecov/c/github/nichelia/nwa?label=code%20coverage)](https://codecov.io/gh/nichelia/nwa)\n[![code alerts](https://badgen.net/lgtm/alerts/g/nichelia/nwa?label=code%20alerts)](https://lgtm.com/projects/g/nichelia/nwa/alerts/)\n[![code quality](https://badgen.net/lgtm/grade/g/nichelia/nwa?label=code%20quality)](https://lgtm.com/projects/g/nichelia/nwa/context:python)\n[![code style](https://badgen.net/badge/code%20style/black/color=black)](https://github.com/ambv/black)\n\n# nwa\nnwa: A collection of network analyses\n\n## Contents\n1. [Use Case](#use-case)\n2. [Configuration](#configuration)\n3. [Development](#development)\n4. [Testing](#testing)\n5. [Versioning](#versioning)\n6. [Deployment](#deployment)\n7. [Production](#production)\n\n## Use Case\n\nA collection of network analyses implementations.  \nInput: [TODO].  \nOutput: [TODO].\n\n### Requirements\n\n* [TODO]\n\n### Assumptions\n\n* [TODO]\n\n### Design\n\n[TODO]\n\n## Configuration\n\nBehaviour of the application can be configured via Environment Variables.\n\n| Environment Variable | Description | Type | Default Value |\n| -------------- | -------------- | -------------- | -------------- |\n| `NWA_LOG_LEVEL` | Level of logging - overrides verbose/quiet flag | string | - |\n| `NWA_LOG_DIR` | Directory to save logs | string | - |\n| `NWA_BIN_DIR` | Directory to save any output (bin) | string | bin |\n\n## Development\n\n### Configure for local development\n\n* Clone [repo](https://github.com/nichelia/nwa) on your local machine\n* Install [`conda`](https://www.anaconda.com) or [`miniconda`](https://docs.conda.io/en/latest/miniconda.html)\n* Create your local project environment (based on [`conda`](https://www.anaconda.com), [`poetry`](https://python-poetry.org), [`pre-commit`](https://pre-commit.com)):  \n`$ make env`\n* (Optional) Update existing local project environment:  \n`$ make env-update`\n\n### Run locally\n\nOn a terminal, run the following (execute on project's root directory):\n\n* Activate project environment:  \n`$ . ./scripts/helpers/environment.sh`\n* Run the CLI using `poetry`:  \n`$ poetry run nwa`\n\n### Contribute\n\n[ Not Available ]\n\n## Testing\n(part of CI/CD)\n\n[ Work in progress... ]\n\nTo run the tests, open a terminal and run the following (execute on project's root directory):\n\n* Activate project environment:  \n`$ . ./scripts/helpers/environment.sh`\n* To run pytest:  \n`$ make test`\n* To check test coverage:  \n`$ make test-coverage`\n\n## Versioning\n\nIncrement the version number:  \n`$ poetry version {bump rule}`  \nwhere valid bump rules are:\n\n1. patch\n2. minor\n3. major\n4. prepatch\n5. preminor\n6. premajor\n7. prerelease\n\n### Changelog\n\nUse `CHANGELOG.md` to track the evolution of this package.  \nThe `[UNRELEASED]` tag at the top of the file should always be there to log the work until a release occurs.  \n\nWork should be logged under one of the following subtitles:\n* Added\n* Changed\n* Fixed\n* Removed\n\nOn a release, a version of the following format should be added to all the current unreleased changes in the file.  \n`## [major.minor.patch] - YYYY-MM-DD`\n\n## Deployment\n\n### Pip package\n\nOn a terminal, run the following (execute on project's root directory):\n\n* Activate project environment:  \n`$ . ./scripts/helpers/environment.sh`\n* To build pip package:  \n`$ make build-package`\n* To publish pip package (requires credentials to PyPi):  \n`$ make publish-package`\n\n### Docker image\n\nOn a terminal, run the following (execute on project's root directory):\n\n* Activate project environment:  \n`$ . ./scripts/helpers/environment.sh`\n* To build docker image:  \n`$ make build-docker`\n\n## Production\n\nFor production, a Docker image is used.\nThis image is published publicly on [docker hub](https://hub.docker.com/repository/docker/nichelia/nwa).\n\n* First pull image from docker hub:  \n`$ docker pull nichelia/nwa:[version]`\n* First pull image from docker hub:  \n`$ docker run --rm -it -v ~/nwa_bin:/usr/src/bin nichelia/nwa:[version]`  \nThis command mounts the application's bin (outcome) to user's root directory under nwa_bin folder.\n\nwhere version is the published application version (e.g. 0.1.0)\n",
    'author': 'Nicholas Elia',
    'author_email': 'me@nichelia.com',
    'maintainer': 'Nicholas Elia',
    'maintainer_email': 'me@nichelia.com',
    'url': 'https://github.com/nichelia/nwa',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
