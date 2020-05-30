#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
    NASA
    ~~~~

    Network Attached Storage Agent
"""

from setuptools import setup, find_packages

__version__ = '0.0.1'
__author__ = 'Albert Moky'
__contact__ = 'albert.moky@gmail.com'

with open('README.md', 'r') as fh:
    readme = fh.read()

setup(
    name='nasa',
    version=__version__,
    url='https://github.com/dimchat/',
    license='MIT',
    author=__author__,
    author_email=__contact__,
    description='Network Attached Storage Agent',
    long_description=readme,
    long_description_content_type='text/markdown',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    install_requires=[
        # 'udp>=0.1.3',
        'stun>=0.1.4',
        'dmtp>=0.1.2',
        # 'mkm>=0.9.3',
        # 'dkd>=0.7.3',
        # 'dimp>=0.9.5',
        'dimsdk>=0.4.3',
    ],
    entry_points={
        'console_scripts': [
            'nasad=nasa.daemon:main'
        ]
    }
)
