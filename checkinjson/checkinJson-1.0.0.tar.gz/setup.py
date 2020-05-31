# coding:utf-8

'''
@author:    chendaben(vida112728@gmail.com)

@Description:
'''

from setuptools import setup, find_packages

setup(
    name = "checkinJson",
    version = "1.0.0",
    keywords = "checkinJson",
    license = "MIT License",
    packages = find_packages(),
    include_package_data = True,
    platforms = "any",
    install_requires = [
        'pprint',
    ],
)