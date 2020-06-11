#!/usr/bin/env python
from setuptools import setup, Extension
# JUST A COMMENT
# JUST ANOTHER COMMENT
try:
    long_description = open('README.md', 'r').read()
except:
    long_description = ''

setup(
    name='query-client-silverbullet-s',
    version='1.0.1',
    packages=['samp_client-ES'],
    url='https://github.com/thenooblol2003/samp-client-s',
    download_url='https://github.com/thenooblol2003/samp-client-s/archive/1.0.1.tar.gz',
    license='MIT',
    author='Michal Dabski',
    author_email='contact@michaldabski.com',
    long_description_content_type='text/markdown',
    install_requires=['future'],
    description='SA-MP API client for python supporting both query and RCON APIs',
    long_description=long_description,
)
