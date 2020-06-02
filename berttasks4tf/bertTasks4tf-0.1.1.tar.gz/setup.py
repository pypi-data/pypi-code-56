#!/usr/bin/python
# coding:utf8
"""
@author: Cong Yu
@time: 2020-05-15 17:16
"""
from setuptools import setup, find_packages

setup(
    name='bertTasks4tf',
    version='0.1.1',
    description='bert tasks 4 tf 1.12+ ',
    long_description='bert4tf: https://github.com/YC-wind/bert4tf',
    license='Apache License 2.0',
    url='https://github.com/YC-wind/bert4tf',
    author='YC-wind',
    author_email='congyu93@foxmail.com',
    install_requires=["pandas", "numpy", "scikit-learn"],
    extras_require={
        'gpu': ["tensorflow-gpu>1.3.0,<2.0.0"],
        'cpu': ['tensorflow>1.3.0,<2.0.0']
    },
    packages=find_packages()
)
