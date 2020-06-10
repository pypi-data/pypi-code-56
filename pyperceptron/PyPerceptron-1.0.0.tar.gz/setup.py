from distutils.core import setup
import setuptools

setup(
  name = 'PyPerceptron',
  packages = ["Perceptron"],
  version = '1.0.0',
  license='MIT',
  description = 'A python implementation of the build block of the Neural Network, The Perceptron',
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