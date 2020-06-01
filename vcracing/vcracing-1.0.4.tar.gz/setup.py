# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
 

setup(
    name='vcracing',
    version='1.0.4',
    description='Enjoy car(?) racing game. Please see https://vigne-cla.com/vc-racing/',
    long_description='Private Use, Commercial Use are permitted. \
    Dont forget Copyright notice (e.g. https://vigne-cla.com/vc-racing/) in any social outputs. Thank you. \
    Required: Copyright notice in any social outputs. \
    Permitted: Private Use, Commercial Use. \
    Forbidden: Sublicense, Modifications, Distribution, Patent Grant, Use Trademark, Hold Liable.',
    author='Shoya Yasuda @ Viniette&Clarity',
    author_email='yasuda@vigne-cla.com',
    url='https://vigne-cla.com/vc-racing/',
    license='Required: Copyright notice in any social outputs. \
    Permitted: Private Use, Commercial Use. \
    Forbidden: Sublicense, Modifications, Distribution, Patent Grant, Use Trademark, Hold Liable.',
    packages=find_packages(),
    install_requires=['numpy', 'matplotlib', 'shapely', 'pillow'],
    package_dir={'vcracing': 'vcracing'},
    package_data={'vcracing': ['data/*.png']},
)