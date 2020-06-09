# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['gilot']

package_data = \
{'': ['*']}

install_requires = \
['GitPython>=3.1.3,<4.0.0',
 'argparse>=1.4.0,<2.0.0',
 'datetime>=4.3,<5.0',
 'matplotlib>=3.2.1,<4.0.0',
 'numpy>=1.18.5,<2.0.0',
 'pandas>=1.0.4,<2.0.0',
 'seaborn>=0.10.1,<0.11.0']

entry_points = \
{'console_scripts': ['gilot = gilot.app:main']}

setup_kwargs = {
    'name': 'gilot',
    'version': '0.1.3',
    'description': 'a git log visual analyzer',
    'long_description': None,
    'author': 'hirokidaichi',
    'author_email': 'hirokidaichi@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
