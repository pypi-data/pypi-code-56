#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun  8 13:55:12 2020

@author: karthikmudlapur
"""
from setuptools import setup, find_packages

with open("README.md", "r") as readme_file:
    readme = readme_file.read()

requirements = ["pandas>=1.0.4", "numpy>=1.18.5", "matplotlib>=3.2.1", "seaborn>=0.10.1"]

setup(
    name="dataeda",
    version="0.0.1",
    author="Karthik Mudlapur",
    author_email="karthikm.39546.km@gmail.com",
    description="A package to that does Exploratry Data Analysis for you",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/edatoall/dataeda",
    packages=find_packages(),
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    ],
)