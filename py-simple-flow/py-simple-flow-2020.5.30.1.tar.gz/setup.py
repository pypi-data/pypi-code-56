# -*- coding: utf-8 -*-
from distutils.core import setup

from setuptools import find_packages

setup(
    name='py-simple-flow',
    packages=find_packages(exclude=('tests',)),
    version='2020.05.30.1',
    description='Simple data processing (ETL) library with support for multi-processing',
    long_description='''### Python Simple Flow 
    - Simple framework with a defined structure for data processing
    - Data processing flow is split into three phases:
        - Ingress
        - Transform
        - Egress
    - Processing can be done in one process, like running it in-process or in multi processing mode
    - Mode to be chosen depends on the task you are doing
    - For processing input from a source with support for multi-processing
    ''',
    long_description_content_type="text/markdown",
    author='Nikhil K Madhusudhan (nikhilkmdev)',
    author_email='nikhilkmdev@gmail.com',
    maintainer='Nikhil K Madhusudhan (nikhilkmdev)',
    maintainer_email='nikhilkmdev@gmail.com',
    install_requires=[],
    keywords=['etl', 'multi processing', 'data', 'processing', 'data processing', 'data flow', 'python3'],
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
)
