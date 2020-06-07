import codecs
import os
import sys
try:
	from setuptools import setup, find_packages
except ImportError:
	from distutils.core import setup, find_packages

def read(fname):
    return codecs.open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(name = 'VTEReportsAnalysis',
      description = 'A Python implementation of simpleNLP algorithm',
      long_description = read("README.md"),
      version = '1.02',
      author = 'Jingxian You',
      author_email = 'jingxian.you@nhs.net',
      packages = find_packages(),
      url = "https://github.com/ykevingrox/VTEReports",
      
      package_data={
              'simpleNLP': ['*'],
              },
      include_package_data=True,
      )