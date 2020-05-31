from setuptools import setup

from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


setup(name='probability_distro',
      version='0.1.3',
      description='Gaussian and Binomal distributions',
      long_description=long_description,
      long_description_content_type='text/markdown',
      packages=['probability_distro'],
      author = "Vamsi Krishna Gutha",
      author_email  = "vamsigutha27@gmail.com",
      url = "https://github.com/vamsigutha/probability-distro",
      zip_safe=False)
