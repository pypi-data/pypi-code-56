#!/usr/bin/env python
"""scrapli_ssh2 - ssh2-python transport plugin for scrapli"""
import setuptools

from scrapli_ssh2 import __version__

__author__ = "Carl Montanari"

with open("README.md", "r", encoding="utf-8") as f:
    README = f.read()

setuptools.setup(
    name="scrapli_ssh2",
    version=__version__,
    author=__author__,
    author_email="carl.r.montanari@gmail.com",
    description="ssh2-python transport plugin for the scrapli SSH|Telnet screen scraping library",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/carlmontanari/scrapli_paramiko",
    packages=setuptools.find_packages(),
    install_requires=["ssh2-python>=0.18.0-1"],
    extras_require={},
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Operating System :: POSIX :: Linux",
        "Operating System :: MacOS",
    ],
    python_requires=">=3.6",
)
