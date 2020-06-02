#!/usr/bin/python
# -*- coding: utf-8 -*-

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='DS1631',
    version='0.3.7',
    py_modules=['DS1631'],
    description='Raspberry pi i2c driver for Maxim-Dallas DS1621 \
DS1631 DS1631A DS1721 DS1731 digital thermometer and thermostat.',
    author='Fabrice Sincère',
    author_email='fabrice.sincere@ac-grenoble.fr',
    maintainer='Fabrice Sincère',
    maintainer_email='fabrice.sincere@ac-grenoble.fr',
    url='https://framagit.org/fsincere/ds1631',
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Intended Audience :: Developers",
        "Topic :: System :: Hardware",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    ],
    python_requires='>=3')
