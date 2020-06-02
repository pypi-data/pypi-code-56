#!/usr/bin/python
import versioneer
from setuptools import setup, find_packages


with open('requirements.txt') as f:
    requirements = f.read().splitlines()


setup(
    name='sdccli',
    author='sysdig Inc.',
    author_email='info@sysdig.com',
    license='MIT',
    description='CLI client for Sysdig Cloud',
    url='https://github.com/draios/sysdig-platform-cli',
    packages=find_packages(),
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    entry_points='''
    [console_scripts]
    sdc-cli=sdccli.cli:cli
    ''',
    install_requires=requirements,
    tests_require=['httmock'],
    test_suite="test"
)
