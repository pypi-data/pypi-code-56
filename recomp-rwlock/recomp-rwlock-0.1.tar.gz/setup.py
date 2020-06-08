#!/usr/bin/env python
# -*- coding: utf-8 -*-

import io
import os
import sys
from shutil import rmtree
from setuptools import setup

VERSION = '0.1'

here = os.path.abspath(os.path.dirname(__file__))

# Import the README and use it as the long description.
# Note: this will only work if 'README.md' is present in your MANIFEST.in file!
try:
    with io.open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
        long_description = '\n' + f.read()
        long_description_content_type='text/markdown',
except FileNotFoundError:
    long_description = ''

# Overwrite VERSION, if RELEASE is set in the environment; see Makefile.
if 'RELEASE' in os.environ:
    VERSION = os.environ['RELEASE']


setup(
    name='recomp-rwlock',
    version=VERSION,
    description='A simple library to protect reader/writer access to a file.',
    long_description=long_description,
    url='http://www.recomp.org.uk',
    author='Jacek Cała',
    author_email='Jacek.Cala@ncl.ac.uk',
    python_requires='>=3.6.0',
    packages=['recomp.rwlock'],
    zip_safe=True,
    license='GPLv3',
    classifiers=[
        # Trove classifiers
        # Full list: https://pypi.python.org/pypi?%3Aaction=list_classifiers
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)'
    ],
)



