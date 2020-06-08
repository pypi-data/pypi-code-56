#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

with open("README.md") as f:
    long_description = f.read()

setup(
    name="torloc",
    version='1.0.1',
    description="A Python tool for running Tor services on local ports",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mrgyber/torloc",
    license="MIT",
    author="Nikita Kudryavtsev",
    author_email="mrgyber@mail.ru",
    keywords=["tor", "proxy"],
    python_requires='>=3.4',
    packages=['torloc'],
    data_files=[('', ['README.md', 'LICENSE'])],
    install_requires=['PySocks', 'requests'],
    zip_safe=False,
)
