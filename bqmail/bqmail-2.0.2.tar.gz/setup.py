#!/usr/bin/env python
from setuptools import find_packages, setup
packages = find_packages()

VERSION = "2.0.2"
setup(name='bqmail',
      version=VERSION,
      author='Mijian Xu',
      author_email='gomijianxu@gmail.com',
      license='GPLv3',
      packages=find_packages(),
      package_dir={'bqmail': 'bqmail'},
      package_data={'': ['data/*']},
      install_requires=['obspy', 'pandas'],
      entry_points={'console_scripts': ['get_stations=bqmail.query:get_stations',
                                        'get_events=bqmail.query:get_events']},
      include_package_data=True,
      zip_safe=False
      )
