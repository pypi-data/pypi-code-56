#!/usr/bin/env python
# setup.py generated by flit for tools that don't yet use PEP 517

from distutils.core import setup

packages = \
['mkmr']

package_data = \
{'': ['*']}

install_requires = \
['gitpython>=3.0.0,<4',
 'python-gitlab>=2.0.0,<3',
 'python-editor>=1.0.0,<2',
 'inquirer>=2.6.0,<3',
 'giturlparse>=0.9.0,<1']

entry_points = \
{'console_scripts': ['edmr = mkmr.edmr:main',
                     'mgmr = mkmr.mgmr:main',
                     'mkmr = mkmr.mkmr:main',
                     'vimr = mkmr.vimr:main']}

setup(name='mkmr',
      version='0.0.15',
      description='Collection of tools for dealing with GitLab Merge Requests, with an Alpine flavour.',
      author='Leo',
      author_email='thinkabit.ukim@gmail.com',
      url='https://github.com/maxice8/mkmr',
      packages=packages,
      package_data=package_data,
      install_requires=install_requires,
      entry_points=entry_points,
      python_requires='>=3.8',
     )
