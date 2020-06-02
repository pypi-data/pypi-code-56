#!/usr/bin/env python
# coding=utf-8

from setuptools import setup, find_packages

setup(
    name='Shenma',
    version='0.0.1',
    description=(
        'A custom library for teaching, maintained by CherryXuan'
    ),
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
