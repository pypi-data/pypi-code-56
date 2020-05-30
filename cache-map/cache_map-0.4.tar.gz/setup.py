from setuptools import setup

from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(name='cache_map',
      version='0.4',
      description='Cache Mapping for Direct and LRU mapping.',
      author='Rahul Sunil',
      author_email='rahulsunil2@gmail.com',
      packages=['cache_map'],
      zip_safe=False,
      long_description=long_description,
      long_description_content_type="text/markdown",)