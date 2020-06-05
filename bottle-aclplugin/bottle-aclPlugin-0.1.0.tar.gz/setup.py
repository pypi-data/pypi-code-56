#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

description = "Bottle plugin acl, api access control"
REQUIREMENTS = [i.strip() for i in open("requirements.txt").readlines()]

setup(
    name='bottle-aclPlugin',
    version="0.1.0",
    packages=find_packages(),
    install_requires=REQUIREMENTS,
    description=description,
    author="Xu_beixiong",
    author_email='17610739793@163.com',
    license='MIT',
    url='https://github.com/bottlepy/bottle-beaker',
    py_modules=['bottle-aclPlugin'],
    requires=['bottle (>=0.9)'],
    classifiers=[
        'Environment :: Web Environment',
        'Environment :: Plugins',
        'Framework :: Bottle',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.5',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
)
