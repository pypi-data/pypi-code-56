# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['redisbench_admin',
 'redisbench_admin.compare',
 'redisbench_admin.export',
 'redisbench_admin.run',
 'redisbench_admin.run.ftsb_redisearch',
 'redisbench_admin.utils']

package_data = \
{'': ['*']}

install_requires = \
['boto3>=1.13.24,<2.0.0',
 'humanize>=2.4.0,<3.0.0',
 'pandas>=1.0.4,<2.0.0',
 'py_cpuinfo>=5.0.0,<6.0.0',
 'redis>=3.5.3,<4.0.0',
 'requests>=2.23.0,<3.0.0',
 'toml>=0.10.1,<0.11.0',
 'tqdm>=4.46.1,<5.0.0']

entry_points = \
{'console_scripts': ['redisbench-admin = redisbench_admin.cli:main']}

setup_kwargs = {
    'name': 'redisbench-admin',
    'version': '0.1.6',
    'description': 'Redis benchmark run helper. A wrapper around ftsb_redisearch ( future versions will also support redis-benchmark and memtier_benchmark ).',
    'long_description': None,
    'author': 'filipecosta90',
    'author_email': 'filipecosta.90@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
