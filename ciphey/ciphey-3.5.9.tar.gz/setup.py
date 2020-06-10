# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ciphey',
 'ciphey.Decryptor',
 'ciphey.Decryptor.Encoding',
 'ciphey.Decryptor.Hash',
 'ciphey.Decryptor.basicEncryption',
 'ciphey.LanguageChecker',
 'ciphey.neuralNetworkMod']

package_data = \
{'': ['*']}

install_requires = \
['cipheycore>=0.1.4,<0.2.0',
 'cipheydists>=0.2.2,<0.3.0',
 'flake8>=3.8.2,<4.0.0',
 'loguru>=0.5.0,<0.6.0',
 'pylint>=2.5.2,<3.0.0',
 'rich>=1.2.3,<2.0.0',
 'tensorflow>=2.1.0,<3.0.0']

entry_points = \
{'console_scripts': ['ciphey = ciphey.__main__:main']}

setup_kwargs = {
    'name': 'ciphey',
    'version': '3.5.9',
    'description': 'Automated Decryption Tool',
    'long_description': None,
    'author': 'Brandon',
    'author_email': 'brandon@skerritt.blog',
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
