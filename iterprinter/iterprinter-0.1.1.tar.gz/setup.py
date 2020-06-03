import os
import sys
from setuptools import setup, Extension

# https://packaging.python.org/guides/making-a-pypi-friendly-readme/
# read the contents of your README file
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


setup(name='iterprinter',
	version = '0.1.1',
	description = 'An iteration history printer',
	long_description=long_description,
	long_description_content_type='text/markdown',
	author = 'Jeffrey M. Hokanson',
	packages = ['iterprinter'],
	install_requires = [],
	zip_safe = False,
)
