from setuptools import setup
from os import path

with open('README.md') as f:
    long_description = f.read()
    
setup(name='ext-distributions',
      version='1.1',
      author='ishan',
      author_email='ishan2198@hotmail.com',
      description='Gaussian distributions and Binomial distributions',
      long_description=long_description,
      long_description_content_type='text/markdown',
      packages=['ext_distributions'],
      zip_safe=False)
