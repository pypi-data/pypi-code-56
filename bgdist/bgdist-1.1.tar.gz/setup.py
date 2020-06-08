from setuptools import setup

with open('README.md') as f:
    README = f.read()

setup(name='bgdist',
      version='1.1',
      description='A package for Gaussian & Binomial distributions',
      long_description_content_type='text/markdown',
      long_description=README,
      packages=['bgdist'],
      author='Tapajyoti Deb',
      author_email='tapajyotideb@gmail.com',
     zip_safe=False)
