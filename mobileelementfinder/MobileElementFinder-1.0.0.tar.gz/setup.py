from distutils.util import convert_path
from typing import Any, Dict

from setuptools import find_packages, setup
import os

try:
    # for pip >= 10
    from pip._internal.req import parse_requirements
except ImportError:
    # for pip <= 9.0.3
    from pip.req import parse_requirements


# Read versions
MAIN_NS: Dict[str, Any] = {}
VER_PATH = convert_path('me_finder/version.py')
with open(VER_PATH) as ver_file:
    exec(ver_file.read(), MAIN_NS)

setup(name='MobileElementFinder',
      version=MAIN_NS['__version__'],
      description='Mobile Genetic Element prediction',
      long_description_markdown_filename='README.md',
      long_description_content_type='text/markdown',
      url='https://bitbucket.org/mhkj/MobileElementFinder/',
      author='Markus Johansson',
      author_email='markjo@food.dtu.dk',
      license='GPLv3',
      classifiers=[
          'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: 3.7',
          'Programming Language :: Python :: 3.8',
      ],
      entry_points={'console_scripts': ['mefinder=me_finder.cli:cli']},
      include_package_data=True,
      package_data={'me_finder': ['logging.yml', 'config.ini']},
      packages=find_packages(exclude=('tests',)))
