#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @see https://www.cnblogs.com/Barrybl/p/12090534.html
# python setup.py sdist build
# twine upload dist/*
# pip install twine

import io
import os
from setuptools import setup


try:
    here = os.path.abspath(os.path.dirname(__file__))
    with io.open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
        long_description = '\n' + f.read()
except FileNotFoundError:
    long_description = ''


setup(
    name='argoptions',
    version='1.0.1',
    description='see tornado.options',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='wzwjustdoit',
    author_email='wzwjustdoit@163.com',
    maintainer='wzwjustdoit',
    maintainer_email='wzwjustdoit@163.com',
    keywords=['argoptions', 'parser', 'opt', 'options', 'tornado', 'argv', 'sys'],
    platforms=["all"],
    python_requires='>=3.0.0',
    url='https://github.com/wzwjustdoit/argoptions',
    packages=['argoptions', ],
    # If your package is a single module, use this instead of 'packages':
    # py_modules=['argoptions'],

    # entry_points={
    #     'console_scripts': ['mycli=mymodule:cli'],
    # },
    install_requires=[],
    extras_require={},
    include_package_data=True,
    license='MIT',
    classifiers=[
        # Trove classifiers
        # Full list: https://pypi.python.org/pypi?%3Aaction=list_classifiers
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy'
    ],
)
