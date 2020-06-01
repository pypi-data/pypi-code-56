#!/usr/bin/env python3
# coding=utf-8

import os
from setuptools import setup
from glob import glob


version = '1.0.0'


setup(
    name='jutge-relayer',
    packages=['jutge.relayer'],
    install_requires=['jutge-util', 'aioredis', 'websockets'],
    version=version,
    description='Notifications relayer for Jutge.org',
    long_description='Notifications relayer for Jutge.org',
    author='Jordi Petit et al',
    author_email='jpetit@cs.upc.edu',
    url='https://github.com/jutge-org/jutge-relayerr',
    download_url='https://github.com/jutge-org/jutge-relayer/tarball/{}'.format(version),
    keywords=['jutge', 'jutge.org', 'relayer'],
    license='Apache',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Education',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Education',
    ],
    zip_safe=False,
    include_package_data=False,
    setup_requires=['setuptools'],
    entry_points={
        'console_scripts': [
            'jutge-relayer=jutge.relayer:relayer.main',
        ]
    }
)

