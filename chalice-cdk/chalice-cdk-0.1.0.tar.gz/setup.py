# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['chalice_cdk']

package_data = \
{'': ['*']}

install_requires = \
['aws_cdk.aws_s3_assets>=1.42.1,<2.0.0',
 'aws_cdk.core>=1.42.1,<2.0.0',
 'chalice>=1.14.1,<2.0.0']

setup_kwargs = {
    'name': 'chalice-cdk',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Stephan Fitzpatrick',
    'author_email': 'knowsuchagency@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
