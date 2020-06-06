# -*- coding: utf-8 -*-
from distutils.core import setup

with open("README.txt", "r") as fh:
    long_description = fh.read()

setup(
    long_description=long_description,
    long_description_content_type="text/markdown",
    name='geo_calculator',
    package_dir={'': 'src'},
    py_modules=["geo_calculator"],
    version='0.1.5',
    description='Multi function Geo Location calculator',
    author='João Esperancinha',
    author_email='jofisaes@gmail.com',
    url='http://joaofilipesabinoesperancinha.nl/main',
    download_url='https://github.com/user/reponame/archive/v_01.tar.gz',
    keywords=['geo', 'location', 'latitude', 'longitude'],
    install_requires=[
        # 'math',
        # 'random',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
)
