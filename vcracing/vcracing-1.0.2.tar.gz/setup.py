# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
 

setup(
    name='vcracing',
    version='1.0.2',
    description='Enjoy car(?) racing game.',
    long_description='Private Use, Commercial Use are permitted. \
    Dont forget Copyright notice (e.g. https://vigne-cla.com/vc-racing/) in any social outputs. Thank you. \
    Required: Copyright notice in any social outputs. \
    Permitted: Private Use, Commercial Use. \
    Forbidden: Sublicense, Modifications, Distribution, Patent Grant, Use Trademark, Hold Liable.',
    author='Shoya Yasuda @ Viniette&Clarity, Inc.',
    author_email='selamatpagi1124@gmail.com',
    url='https://vigne-cla.com/vc-racing/',
    license='Required: Copyright notice in any social outputs. \
    Permitted: Private Use, Commercial Use. \
    Forbidden: Sublicense, Modifications, Distribution, Patent Grant, Use Trademark, Hold Liable.',
    packages=find_packages(),
    install_requires=['numpy', 'matplotlib', 'shapely', 'pillow'],
    package_data={'vcracing': ['data/*.png']},
)