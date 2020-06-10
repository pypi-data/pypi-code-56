import io
import os
import os.path as osp
import json
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))

NAME = 'pdhttp'
DESCRIPTION = 'Swagger-generated API Client for Pulse Robotic Arm'
URL = 'https://rozum.com'
EMAIL = 'dev@rozum.com'
AUTHOR = 'Rozum Robotics'

with open(osp.join(here, '../configs/urllib/config.json')) as c:
    VERSION = json.loads(''.join(c.readlines()))['packageVersion']

if 'dev' in VERSION:
    DEVELOPMENT_STATUS = 'Development Status :: 4 - Beta'
else:
    DEVELOPMENT_STATUS = 'Development Status :: 5 - Production/Stable'

REQUIRED = [
    "certifi>=2017.4.17",
    "python-dateutil>=2.1",
    "six>=1.10",
    "urllib3>=1.23"
]

# Import the README and use it as the long-description.
# Note: this will only work if 'README.md' is present in your MANIFEST.in file!
try:
    with io.open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
        long_description = '\n' + f.read()
except FileNotFoundError:
    long_description = DESCRIPTION

setup(
    name=NAME,
    version=VERSION,
    packages=[p for p in find_packages() if 'test' not in p],
    install_requires=REQUIRED,
    url=URL,
    license='Apache License 2.0',
    classifiers=[
        'License :: OSI Approved :: Apache Software License',
        DEVELOPMENT_STATUS,
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: Implementation :: CPython'
    ],
    author=AUTHOR,
    author_email=EMAIL,
    description=DESCRIPTION,
    zip_safe=False
)
