import codecs
import os
import sys

try:
    from setuptools import setup
except:
    from distutils.core import setup


def read(fname):
    return codecs.open(os.path.join(os.path.dirname(__file__), fname)).read()


NAME = "fbobo_test"
PACKAGES = ['test']
DESCRIPTION = "this is a test for package by myself upload to pypi"
LONG_DESCRIPTION = "this is a test for package by myself upload to pypi"
KEYWORDS = "keyword"
AUTHOR = "feikong"
AUTHOR_EMAIL = "feikong@shouxin168.com"
URL = "https://github.com/lichanghong/wenyali.git"
VERSION = "1.0.0"
LICENSE = "MIT"
setup(
    name=NAME, version=VERSION,
    description = DESCRIPTION,long_description =LONG_DESCRIPTION,
    classifiers =[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
    ],
    keywords =KEYWORDS,author = AUTHOR,
    author_email = AUTHOR_EMAIL,url = URL, 
    packages = PACKAGES,include_package_data=True,zip_safe=True,
    entry_points={
      "console_scripts": [
                          "wenyali_console = package1.index:index",
                          ]
      },

)