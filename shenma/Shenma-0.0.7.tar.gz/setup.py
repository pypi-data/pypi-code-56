#!/usr/bin/env python
# coding=utf-8

from setuptools import setup, find_packages

# read the contents of your README file
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


setup(
    name='Shenma',
    version='0.0.7',
    description=(
        'A custom library for teaching, maintained by CherryXuan'
    ),
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='CherryXuan',
    author_email='shenzexuan1994@foxmail.com',
    maintainer='CherryXuan',
    maintainer_email='shenzexuan1994@foxmail.com',
    license='MIT Licence',
    packages=find_packages(),
    platforms=["all"],
    url='https://gitee.com/cherryxuan/SpeechRecognition',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries'
    ],
    install_requires=[
        'numpy>=1.14.0',
        'matplotlib>=2.1.2',
        'PyAudio>=0.2.11',
    ],
)
