from setuptools import setup

import os
import re

__version__ = '0.1'

setup(
    name='pumpit',
    version=__version__,
    packages=[
        'pumpit',
    ],
    author='Thomas Oberbichler',
    author_email='thomas.oberbichler@gmail.com',
    install_requires=[
        'click'
    ],
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'pumpit=pumpit.__main__:main'
        ]
    }
)
