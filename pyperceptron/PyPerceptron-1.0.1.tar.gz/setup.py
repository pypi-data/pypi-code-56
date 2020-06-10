from setuptools import setup

# read the contents of your README file
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
  name = 'PyPerceptron',
  packages = ["Perceptron"],
  version = '1.0.1',
  license='MIT',
  description = 'A python implementation of the build block of the Neural Network, The Perceptron',
  long_description = long_description,
  long_description_content_type="text/markdown",
  author = 'Paolo D\'Elia',
  author_email = 'paolo.delia99@gmail.com',
  url = 'https://github.com/paolodelia99/Python-Perceptron',
  keywords = ['Perceptron', 'Neural Net', 'Machine learning'],   #
  install_requires=[
          'numpy',
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
  ],
  project_urls={
    'Demo': 'https://github.com/paolodelia99/Python-Perceptron/tree/master/demo',
    'Repo': 'https://github.com/paolodelia99/Python-Perceptron',
  },
)