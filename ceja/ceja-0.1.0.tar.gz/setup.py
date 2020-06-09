# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ceja']

package_data = \
{'': ['*']}

install_requires = \
['jellyfish>=0.8.2,<0.9.0', 'pyspark>=2.4.6,<3.0.0']

setup_kwargs = {
    'name': 'ceja',
    'version': '0.1.0',
    'description': 'PySpark string and phonetic matching',
    'long_description': None,
    'author': 'MrPowers',
    'author_email': 'matthewkevinpowers@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
