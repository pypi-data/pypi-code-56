# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

modules = \
['s3bucketencryptor']
install_requires = \
['boto3>=1.13.21,<2.0.0']

entry_points = \
{'console_scripts': ['s3enc = s3bucketencryptor:encrypt_bucket']}

setup_kwargs = {
    'name': 's3bucketencryptor',
    'version': '0.1.1',
    'description': 'It sets Server Side Encryption as AES256 for Objects in a S3 Bucket.',
    'long_description': None,
    'author': 'oi73ooh',
    'author_email': 'cindian@amazingbutuseless.net',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
