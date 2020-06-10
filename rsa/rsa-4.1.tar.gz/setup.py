# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': '.'}

packages = \
['rsa']

package_data = \
{'': ['*']}

install_requires = \
['pyasn1>=0.1.3']

extras_require = \
{':python_version >= "3.5" and python_version < "3.6"': ['pysha3>=1.0,<2.0']}

entry_points = \
{'console_scripts': ['pyrsa-decrypt = rsa.cli:decrypt',
                     'pyrsa-encrypt = rsa.cli:encrypt',
                     'pyrsa-keygen = rsa.cli:keygen',
                     'pyrsa-priv2pub = rsa.util:private_to_public',
                     'pyrsa-sign = rsa.cli:sign',
                     'pyrsa-verify = rsa.cli:verify']}

setup_kwargs = {
    'name': 'rsa',
    'version': '4.1',
    'description': 'Pure-Python RSA implementation',
    'long_description': None,
    'author': 'Sybren A. Stüvel',
    'author_email': 'sybren@stuvel.eu',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://stuvel.eu/rsa',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
