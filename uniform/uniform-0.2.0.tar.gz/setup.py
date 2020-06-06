#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re

from setuptools import find_packages, setup


def get_version(package):
    """
    Return package version as listed in `__version__` in `__version__.py`.
    """
    with open(os.path.join(package, "__version__.py")) as f:
        return re.search("__version__ = ['\"]([^'\"]+)['\"]", f.read()).group(1)


def get_long_description():
    """
    Return the README.
    """
    with open("README.md", encoding="utf8") as f:
        return f.read()


setup(
    name="uniform",
    python_requires=">=3.6",
    version=get_version("uniform"),
    url="https://gitlab.com/not-good-igor/uniform.py",
    license="Unlicense",
    description="Uniform - dress your form processing endpoints📋",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    author="Igor Nehoroshev",
    author_email="mail@neigor.me",
    packages=["uniform"],
    data_files=[("", ["LICENSE"])],
    include_package_data=True,
    install_requires=["typesystem", "starlette",],
    extras_require={
        "test": ["asynctest", "httpx"],
        "lint": ["mypy", "autoflake", "black", "isort"],
    },
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: Public Domain",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
)
