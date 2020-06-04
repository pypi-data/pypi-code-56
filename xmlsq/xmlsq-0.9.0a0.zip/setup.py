from setuptools import setup
import os


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


readme = read('README.rst')
changelog = read('CHANGELOG.rst')

setup(name='xmlsq',
      version='0.9.0a',
      description='A Python interface to xmlsq.',
      long_description=readme,
      author='David Ireland',
      url='https://www.cryptosys.net/xmlsq/',
      platforms=['Windows'],
      py_modules=['xmlsq'],
      )
