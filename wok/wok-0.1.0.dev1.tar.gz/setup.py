# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tests', 'wok', 'wok.config', 'wok.core']

package_data = \
{'': ['*'],
 'tests': ['data/*',
           'data/repos/prj-1/*',
           'data/repos/prj-1/hooks/*',
           'data/repos/prj-1/info/*',
           'data/repos/prj-1/objects/5c/*',
           'data/repos/prj-1/objects/8d/*',
           'data/repos/prj-1/objects/a2/*',
           'data/repos/prj-1/objects/e6/*',
           'data/repos/prj-1/objects/f3/*',
           'data/repos/prj-1/objects/pack/*',
           'data/repos/prj-1/refs/heads/*',
           'data/repos/prj-2/*',
           'data/repos/prj-2/hooks/*',
           'data/repos/prj-2/info/*',
           'data/repos/prj-2/objects/6e/*',
           'data/repos/prj-2/objects/88/*',
           'data/repos/prj-2/objects/b4/*',
           'data/repos/prj-2/objects/dd/*',
           'data/repos/prj-2/objects/e6/*',
           'data/repos/prj-2/objects/pack/*',
           'data/repos/prj-2/refs/heads/*',
           'data/repos/workspace/*',
           'data/repos/workspace/hooks/*',
           'data/repos/workspace/info/*',
           'data/repos/workspace/objects/3c/*',
           'data/repos/workspace/objects/69/*',
           'data/repos/workspace/objects/f6/*',
           'data/repos/workspace/objects/pack/*',
           'data/repos/workspace/refs/heads/*']}

install_requires = \
['attrs>=19.3.0,<20.0.0',
 'cached-property>=1.5.1,<2.0.0',
 'cffi>=1.14.0,<2.0.0',
 'click>=7.0,<8.0',
 'marshmallow>=3.5.1,<4.0.0',
 'pygit2>=1.1.1,<2.0.0',
 'pyyaml>=5.3.1,<6.0.0',
 'toml>=0.10.0,<0.11.0']

entry_points = \
{'console_scripts': ['wok = wok.cli:main']}

setup_kwargs = {
    'name': 'wok',
    'version': '0.1.0.dev1',
    'description': 'Wok is a tool to manage several `git` repos in a single workspace.',
    'long_description': None,
    'author': 'Serge Matveenko',
    'author_email': 'lig@countzero.co',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
