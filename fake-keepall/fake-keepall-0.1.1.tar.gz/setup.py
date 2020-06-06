# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fake_keepall']

package_data = \
{'': ['*']}

install_requires = \
['beautifulsoup4>=4.9.1,<5.0.0', 'click>=7.1.2,<8.0.0']

entry_points = \
{'console_scripts': ['fake-keepall = fake_keepall.__init__:cli']}

setup_kwargs = {
    'name': 'fake-keepall',
    'version': '0.1.1',
    'description': 'Apply the fake `word-break: keep-all;` CSS property to static HTML file',
    'long_description': "# Fake KeepAll\n\nApply the fake `word-break: keep-all;` CSS property to static HTML file.\n\nThis is useful when using the HTML->PDF converter that does not support the `word-break: keep-all;` CSS property.\n\n## How it works\n\nAdd the `white-space: nowrap;` CSS property to every word to prevent line breaks.\n\n## Installation\n\n```bash\n$ pip install fake-keepall\n```\n\n## Usage\n\n```bash\n$ fake-keepall example.html --out example_out.html\n```\n\nSet whitelist tags:\n\n```bash\n$ fake-keepall example.html --out example_out.html --tags 'p,li'\n```\n\nUse custom CSS class:\n\n```bash\n$ fake-keepall example.html --out example_out.html --class 'myclass'\n```\n\n## Screenshot\n\n![screenshot](screenshot.png)\n\n",
    'author': 'Chanwoong Kim',
    'author_email': 'me@chanwoong.kim',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/kexplo/fake_keepall',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.0.0,<4.0.0',
}


setup(**setup_kwargs)
