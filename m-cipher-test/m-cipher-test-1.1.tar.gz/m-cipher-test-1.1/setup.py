#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" Author: ChungNT
    Company: MobioVN
    Date created: 05/06/2020
"""
import os

from distutils.core import setup, Extension

SOURCE_PATH = 'mobio'


def package_files(directory, ext=None):
    paths = []
    for (path, directories, filenames) in os.walk(directory):
        for filename in filenames:
            if filename.endswith(ext):
                paths.append(os.path.join(path, filename))
    return paths


extra_files = package_files('mobio', '.c')

module1 = Extension('mobio.libs.ciphers.__init__', sources=extra_files)

setup(
    name='m-cipher-test',
    version='1.1',
    author='Mobio Company',
    author_email='contact@mobio.vn',
    ext_modules=[module1]
)
