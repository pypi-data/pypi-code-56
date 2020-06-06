# -*- coding: utf-8 -*-
"""
Setup
-----
Install kafkaconnectsync in the current python environment.
"""
# ----------------------------------------------------------------------------
# Imports
# ----------------------------------------------------------------------------


# ---- Future
from __future__ import print_function
from __future__ import with_statement

# ---- System
import os
from setuptools import setup

# ----------------------------------------------------------------------------
# Helper Functions
# ----------------------------------------------------------------------------


def file_contents(file_name):
    """Given a file name to a valid file returns the file object."""
    curr_dir = os.path.abspath(os.path.dirname(__file__))
    with open(os.path.join(curr_dir, file_name)) as the_file:
        contents = the_file.read()
    return contents

# ----------------------------------------------------------------------------
# Setup
# ----------------------------------------------------------------------------


setup(
    name='kafkaconnectsync',
    version='0.0.1',
    description="Kafka Connect API connectors synchronization library",
    long_description=file_contents("README.md"),
    long_description_content_type='text/markdown',

    author="Christopher Ventura",
    author_email="chrisventura.work@gmail.com",
    license="MIT license",
    url="https://github.com/venturachrisdev/kafka-connect-sync",

    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",

        "License :: OSI Approved :: MIT License",

        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX :: BSD",
        "Operating System :: POSIX :: Linux",

        "Programming Language :: Python",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 2.7",
    ],

    packages=[
        'kafkaconnectsync',
    ],
    python_requires=">=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*",
    install_requires=file_contents("requirements.txt"),
    test_suite="tests",
    tests_require=[],
    extras_require={},

    use_2to3=True,
)
