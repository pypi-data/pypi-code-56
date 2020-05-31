#!/usr/bin/env python
"""
# Copyright © Nico Huebschmann
# Licensed under the terms of the MIT License
"""

from setuptools import setup, find_packages

setup(name='drf-rest-auth',
      version='1.0.0',
      license='MIT',
      author='Nico Huebschmann',
      author_email='nico_huebschmann@web.de',
      python_requires='>=3.6.0',
      url='https://github.com/LiQuitCore/drf-rest-auth',
      download_url = 'https://github.com/LiQuitCore/drf-rest-auth/archive/v1.0.0.tar.gz',
      description='Offers a set of REST API endpoints for authentication',
      platforms='any',
      packages=find_packages(exclude=['tests']),
      keywords=['django', 'rest-framework', 'REST', 'auth', 'JWT', 'authentication'],
      install_requires=[
          'Django>=3.0.4',
          'djangorestframework>=3.11.0',
          'djangorestframework-jwt>=1.11.0',
      ],
      classifiers=[
          'Framework :: Django',
          'Intended Audience :: Developers',
          'Intended Audience :: System Administrators',
          'Operating System :: OS Independent',
          'Topic :: Software Development',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 3',
      ],
      )
