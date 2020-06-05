#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" Author: ChungNT
    Company: MobioVN
    Date created: 05/06/2020
"""
import os

from setuptools import setup
from Cython.Build import cythonize

SOURCE_PATH = 'mobio'


def package_files(directory):
    paths = []
    for (path, directories, filenames) in os.walk(directory):
        for filename in filenames:
            paths.append(os.path.join('..', path, filename))
    return paths


extra_files = package_files('mobio')

setup(
    name='m-cipher',
    version='1.3',
    author='Mobio Company',
    author_email='contact@mobio.vn',
    packages=['mobio/libs/ciphers'],
    ext_modules=cythonize([SOURCE_PATH + '/**/*.py'], compiler_directives=dict(always_allow_keywords=True)),
    install_requires=[
                      'Crypto',
                      'numpy',
                      ],
    package_data={'': extra_files},
    include_package_data=True
)
