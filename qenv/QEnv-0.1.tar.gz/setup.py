from setuptools import setup

with open('README.md') as f:
    long_description = f.read()

setup(
  name = 'QEnv',
  packages = ['QEnv'],
  version = '0.1',
  license='MIT',
  description = 'Utilities for programming at QEGS Faversham',
  author = 'Quentin \'Q\' Thomas A.K.A Shaun Cameron',
  author_email = 'libnexus.theprogrammer@gmail.com',
  url = 'http://lib-nexus.github.io/site/docs/QEnv',
  keywords = ['QE', 'QGESF', 'FAVERSHAM', 'QUEENELIZABETHS', 'QUENTIN'],
  long_description=long_description,
  long_description_content_type='text/markdown',  
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
  ],
)