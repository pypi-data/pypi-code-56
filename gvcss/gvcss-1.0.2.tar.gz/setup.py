# -*- coding: UTF-8 -*-

from setuptools import setup, find_packages
import os


here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'readme.md')) as f:
    README = f.read()
setup(
    name='gvcss',    
    version='1.0.2',   
    python_requires="<3",
    description='gvcss is single sample somatic mutations (SNV, InDel, SV) from FASTQ files.',  
    author='bob zhang',  
    author_email='bob.zhang@genowis.com',
    long_description=README,
    long_description_content_type="text/plain",
    packages=find_packages(),                 
    install_requires=['toil==3.19.0', 'gvc4fastq','docker==2.5.1', 'toil-runner'],
    classifiers=['Programming Language :: Python :: 2.7','License :: Free For Educational Use'],
    scripts=['gvcss_cli.py']
)
