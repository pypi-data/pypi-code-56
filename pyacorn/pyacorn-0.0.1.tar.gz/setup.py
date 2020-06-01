# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
from glob import glob
from os import path

parent = path.abspath(path.dirname(__file__))
with open(path.join(parent, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='pyacorn',
    version='0.0.1',
    description="The python command-line client for the acorn platform",
    long_description=long_description,
    keywords='python acorn cli',
    project_urls={},
    packages=find_packages(exclude=['tests']),
    install_requires=[
        'requests>=2.22.0,<3',
        'click>=7.1.1,<8',
        'pyfiglet',
    ],
    python_requires='>=3.5,<4',
    entry_points={
        'console_scripts': [
            'pyacorn = pyacorn.client:cli',
        ],
    }
)