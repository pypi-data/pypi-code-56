#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" Author: ChungNT
    Company: MobioVN
    Date created: 05/06/2020
"""

from setuptools import setup
from Cython.Build import cythonize

SOURCE_PATH = './mobio/'

setup(
    name='m-cipher',
    version='1.1',
    packages=[''],
    author='Mobio Company',
    author_email='contact@mobio.vn',
    ext_modules=cythonize([SOURCE_PATH + '/**/*.py'], compiler_directives=dict(always_allow_keywords=True)),
    install_requires=[
                      'Crypto',
                      'numpy',
                      ]
    )
