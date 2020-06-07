# -*- coding: utf-8 -*-#
"""
@author:Galen.Wang
@file: setup.py.py
@time: 2020/6/2
@description:
Great artist always hid themselves in their work.

"""

from setuptools import setup, find_packages

VERSION = '0.0.2'
with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='ducut',
    version=VERSION,
    description='ducut',
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="Apache-2.0",
    author='galen',
    author_email='mywayking@icloud.com',
    classifiers=[
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Intended Audience :: Science/Research',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    url='https://github.com/Mywayking/',
    keywords='word cut for du',
    py_modules=['ducut'],
    packages=find_packages(),
    install_requires=[
        'jieba',
    ],
    # package_data={
    #     'ducut': ['data/word_dict/*.txt', 'data/word_dict/*.csv'],
    # },
    python_requires='>=3.4',
)
