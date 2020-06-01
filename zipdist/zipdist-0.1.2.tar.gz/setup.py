from setuptools import setup, find_packages
PACKAGES = find_packages()

# read the contents of your README file
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

opts = dict(name='zipdist',
            maintainer='Koshlan Mayer-Blackwell',
            maintainer_email='kmayerbl@fredhutch.org',
            description='Tidy saving and loading of Numpy and Pandas object attributes',
            long_description=long_description,
            long_description_content_type='text/markdown',
            url='https://github.com/kmayerb/zipdist',
            license='MIT',
            author='Koshlan Mayer-Blackwell',
            author_email='kmayerbl@fredhutch.org',
            version='0.1.2',
            packages=PACKAGES
           )

install_reqs = [
      'numpy>=1.18.1',
      'pandas>=0.24.2']

if __name__ == "__main__":
      setup(**opts, install_requires=install_reqs)
