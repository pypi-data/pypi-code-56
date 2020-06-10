# -*- coding: utf-8 -*-

from setuptools import setup

with open('README.rst', 'r') as f:
    README = f.read()

with open('requirements.txt', 'r') as f:
    install_requires = f.read()

setup(
    name = 'tdms2axg',
    version = '0.2.0',
    description = 'A simple script for converting LabVIEW TDMS files to AxoGraph files',
    packages = ['tdms2axg'],
    install_requires = install_requires,
    entry_points = {'console_scripts': ['tdms2axg=tdms2axg.scripts:main']},
    long_description = README,
    keywords = ['neuroscience', 'electrophysiology', 'National Instruments',
        'LabVIEW', 'tdms', 'AxoGraph', 'axgx', 'axgd'],
    author = 'Jeffrey Gill',
    author_email = 'jeffrey.p.gill@gmail.com',
    license = 'MIT',
    url = 'https://github.com/jpgill86/tdms2axg',
    project_urls = {
        'Source code': 'https://github.com/jpgill86/tdms2axg',
        'Bug tracker': 'https://github.com/jpgill86/tdms2axg/issues',
    },
    classifiers = [
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
