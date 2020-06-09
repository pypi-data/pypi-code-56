#!/usr/bin/env python
#-*- coding:utf-8 -*-

#############################################
# Filename: setup.py
# Author: Chunlei Wang
# Mail: chuwan@microsoft.com
# Created Time:  2020-06-09 19:17:34
#############################################

from setuptools import setup, find_packages

with open("TimeSeriesAnalysisPlugin/README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="time-series-analysis-plugin",
    version="0.0.1",
    keywords = ("pip", "SICA","featureextraction"),
    description = "Time series analysis plugin",
    long_description = "An plugin package for time series analysis, 3rd party could implement their own train/inference.",
    long_description_content_type="text/markdown",
    license = "MIT Licence",
    url = "https://github.com/minkefusiji/TimeSeriesAnalysisPlugin",
    author = "Chunlei Wang",
    author_email = "chuwan@microsoft.com",
    packages = find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)