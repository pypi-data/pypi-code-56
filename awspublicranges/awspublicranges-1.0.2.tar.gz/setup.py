#!/usr/bin/env python3
from setuptools import setup, find_packages

setup(
    name='awspublicranges',
    version='1.0.2',
    python_requires='>=3.6',
    packages=find_packages(exclude=("tests",)),
    install_requires=['requests'],
    setup_requires=['wheel'],
    # Metadata
    author="Matthew G. Monteleone",
    author_email="mgm@mgm.dev",
    license="MIT License",
    description="Simple utility for grabbing and using AWS public IPS",
    long_description=open('README.rst').read(),
    url="https://github.com/mgmonteleone/python-aws-public-ranges",
    keywords=["cloud", "aws"],
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 5 - Production/Stable',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: Apache Software License',

        'Operating System :: OS Independent',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    extras_require={}

)
