#!/usr/bin/env python
#-*- coding:utf-8 -*-
# author:Ruci
# datetime:2020/6/7 11:50
# software: PyCharm


import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="rucicodeapi", # Replace with your own username
    version="1.1",
    author="Ruci",
    author_email="178366124@qq.com",
    description="a code api.",
    # long_description=long_description,
    # long_description_content_type="text/markdown",
    url="https://github.com/",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=['requests'],
    python_requires='>=3.5',
)