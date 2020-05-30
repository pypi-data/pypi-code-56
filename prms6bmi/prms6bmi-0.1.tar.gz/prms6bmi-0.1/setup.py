import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()
    
setuptools.setup(name='prms6bmi',
      version='0.1',
      description='Utilities for working with prms6-bmi I/O',
      long_description = long_description,
      long_description_content_type="text/markdown",
      url='https://github.com/nhm-usgs/bmi-test-projects',
      author='Richard McDonald',
      author_email='rmcd@usgs.gov',
      packages = setuptools.find_packages(),
      license='public domain',
      zip_safe=False)
