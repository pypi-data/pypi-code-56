#!/usr/bin/env python3
import setuptools
import os
with open('README.md') as f:
    long_description = f.read()

setuptools.setup(
      name='anki-kunren',
      version='1.0',
      description='Anki practice tool to drill japanese kanji stroke order and practice writing.',
      long_description=long_description,
      long_description_content_type="text/markdown",
      packages=setuptools.find_packages(),
      python_requires='>=3.6',
      install_requires=['pygame','svg.path'],
      author='esrh',
      author_email='esrh@netc.eu',
      keywords='japanese anki kanji stroke order writing',
      url='https://github.com/eshrh/anki-kunren',
      entry_points={'console_scripts': ['kunren=kunren:main']}
     )
