# -*- coding: utf-8 -*-
from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='lets-debug',
    version='0.0.2',
    url='https://github.com/luizfilipezs/lets-debug',
    license='MIT License',
    author='Luiz Filipe da Silva',
    author_email='filipeluiz.bs@gmail.com',
    keywords='debug tools terminal',
    description=u'Useful tools for debugging Python code',
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=['lets_debug'],
    install_requires=[],
    python_requires='>=3.7.5',
)