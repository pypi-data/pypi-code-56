#!/usr/bin/env python3

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="partsfinder", # Replace with your own username
    version="0.0.6",
    author="Maciej Grela",
    author_email="enki@fsck.pl",
    description="A small example package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mgrela/partsfinder",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha",
        "Topic :: Scientific/Engineering :: Electronic Design Automation (EDA)"
    ],
    python_requires='>=3.7',
    install_requires=[
        'structlog', 'requests', 'requests_toolbelt', 'js2py', 'money', 'pint',
        'beautifulsoup4'
    ]
)
