# -*- coding: utf-8 -*-
# @Time: 2020/6/3 0003
# @Author: gmo_ye
# @Version: 1.0.0
# @Function:
# 参照：https://packaging.python.org/tutorials/packaging-projects/
# !/usr/bin/env python

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='aibase',
    version='0.0.3',
    author='gmo_ye',
    author_email='gmo_ye@163.com',
    description='基础包',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='http://svn.51iwifi.com/repos/AI/bi/code/trunk/aibase',
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=['Pillow>=6.1.0', 'flask>=1.1.1', 'redis>=3.3.11', 'kafka>=1.3.5'],
    python_requires='>=3.6',
)
