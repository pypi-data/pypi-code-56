#!/usr/bin/env python
# Copyright 2020 Alexander Couzens <lynxis@fe80.eu>
#
# License: MIT

from setuptools import setup
import adlinkusb

setup(
    name='adlink-usb',
    version=adlinkusb.__version__,
    description='Adlink USB DAQ driver',
    author='Alexander Couzens',
    author_email='lynxis@fe80.eu',
    url='https://github.com/lynxis/adlinkusb',
    packages=['adlinkusb'],
    long_description=
"""
Adlink USB is a fully open source implementation in python to
control Adlink USB DAQ devices.
""",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: Manufacturing', # USB automation, or mfg USB devs
        # source(CPython,Jython,IronPython,PyPy): "The Long Term" section of
        # http://ojs.pythonpapers.org/index.php/tpp/article/viewFile/23/23
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: IronPython',
        'Programming Language :: Python :: Implementation :: Jython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: System :: Hardware :: Hardware Drivers'
    ],
    python_requires='>=3',
)
