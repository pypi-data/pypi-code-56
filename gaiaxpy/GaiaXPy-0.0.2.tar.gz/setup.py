"""
Setup module for GaiaXPy.

List of authors - 2020

Based on:
https://packaging.python.org/tutorials/packaging-projects
"""

from setuptools import setup, find_packages
import os, sys

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, "README-pypi.rst")).read()
NEWS = open(os.path.join(here, "NEWS.txt")).read()

with open("requirements.txt") as f:
    required_packages = f.readlines()

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="GaiaXPy",
    version="0.0.1",
    author="Francesca De Angeli",
    author_email="fda@ast.cam.ac.uk",
    description="Utilities to handle BP/RP (XP) Gaia low-resolution spectra as delivered via the archive",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="http://gitlab.com/pyxp-developers/pyxp-pkg",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=required_packages
)
