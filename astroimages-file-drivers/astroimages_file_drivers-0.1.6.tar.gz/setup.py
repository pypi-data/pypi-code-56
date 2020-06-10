# -*- coding: utf-8 -*-
# from setuptools import setup, find_packages
import setuptools


with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setuptools.setup(
    name='astroimages_file_drivers',
    version='0.1.6',
    description='File handling routines',
    author='Rodrigo de Souza',
    author_email='rsouza01@gmail.com',
    url='https://github.com/AstroImages/astroimages-file-drivers',
    download_url='https://github.com/AstroImages/astroimages-file-drivers/archive/v_0.1.6.tar.gz',
    license=license,
    install_requires=[
    ],
    packages=setuptools.find_packages(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ]
)
