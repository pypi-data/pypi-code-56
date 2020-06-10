# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['kaomoji']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'kaomoji',
    'version': '0.1.0',
    'description': 'Create procedurally generated kaomoji (i.e., Japanese emoticons) using Python! \\(^ヮ^)/',
    'long_description': '# Kaomoji\n\n> Create procedurally generated kaomoji (i.e., Japanese emoticons) using Python! \\\\(^ヮ^)/\n\n![version](https://img.shields.io/pypi/v/kaomoji?style=for-the-badge)\n![python version](https://img.shields.io/pypi/pyversions/kaomoji?style=for-the-badge)\n![license](https://img.shields.io/pypi/l/kaomoji?style=for-the-badge)\n\nThis Python package uses procedural generation to create _kaomoji_ using a collection of features (e.g., eyes, arms, etc.) across a wide variety of different categories, such as emotions (e.g., joy, indifference, love) and animals (e.g., dog, cat, etc.). Also, the individual _kaomoji_ features and template used to organize the features are fully customizable.\n\n[![asciicast](https://asciinema.org/a/337897.svg?speed=2&theme=monokai)](https://asciinema.org/a/337897)\n\n## Installation\n\nInstallation is easy using the `pip` package manager.\n\n```console\n$ pip install --user kaomoji\n```\n\n## Example\n\nRun the following command on the console to view a pre-fab example.\n\n```console\n$ python -m kaomoji\n```\n\n## Usage\n\nThe first step is to import the `Kaomoji` class.\n\n```python\n> from kaomoji.kaomoji import Kaomoji\n```\n\nNext, instantiate a `Kaomoji` object.\n\n```python\n> kao = Kaomoji()\n```\n\nUsing the `Kaomoji` object, procedurally generate a _kaomoji_ from a random category.\n\n```python\n> kao.create()\n```\n\nOr, generate a _kaomoji_ from a specific category.\n\n```python\n> kao.create("joy")\n```\n\nAll of the available categories are easily viewable on the `categories` attribute.\n\n```python\n> kao.categories\n```\n\n## Releases\n\nThis project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html). See [`CHANGELOG`](./CHANGELOG.md) for a detailed release history.\n\n## Contributing\n\nContributions are welcome. See [`CONTRIBUTING`](./CONTRIBUTING.md) for instructions on how to contribute to this project.\n\n## License\n\nDistributed under the [MIT](https://opensource.org/licenses/MIT) license. See [`LICENSE`](./LICENSE.md) for more information.\n\n## Author\n\nThis project was made with 💖 by Keith Dowd @ <keith.dowd@gmail.com>.\n\n## Acknowledgements\n\nBig thanks to [Japan](https://www.japan.go.jp/) for creating _kaomoji_ and anime.\n\nAlso, huge shoutout to [kaomoji.ru](http://kaomoji.ru/en/) for the history and wonderfully expansive and organized collection of _kaomoji_.\n',
    'author': 'Keith Dowd',
    'author_email': 'keith.dowd@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/keithdowd/kaomoji',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
