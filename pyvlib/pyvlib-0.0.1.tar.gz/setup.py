# -*- coding: utf-8 -*-

# modified from https://github.com/vchoutas/smplx

import io
import os

from setuptools import setup, find_packages

# Package meta-data.
NAME = 'pyvlib'
DESCRIPTION = 'Python vlib'
URL = 'https://github.com/VVingerfly/pyvlib'
EMAIL = 'wei587me@163.com'
AUTHOR = 'Li Wei'
REQUIRES_PYTHON = '>=3.6.0'
VERSION = ''  # defined in version.py

here = os.path.abspath(os.path.dirname(__file__))

try:
    FileNotFoundError
except NameError:
    FileNotFoundError = IOError


# Import the README and use it as the long-description.
# Note: this will only work if 'README.md' is present in your MANIFEST.in file!
try:
    with io.open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
        long_description = '\n' + f.read()
except FileNotFoundError:
    long_description = DESCRIPTION

# Load the package's version.py module as a dictionary.
about = {}
if not VERSION:
    with open(os.path.join(here, NAME, 'version.py')) as f:
        # exec(f.read(), about)
        about['__version__'] = eval(f.read().strip().split('=')[-1])
else:
    about['__version__'] = VERSION

pyrender_reqs = ['pyrender>=0.1.23', 'trimesh>=2.37.6', 'shapely']
matplotlib_reqs = ['matplotlib']
open3d_reqs = ['open3d-python']

setup(
    name=NAME,
    version=about['__version__'],
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type='text/markdown',
    author=AUTHOR,
    author_email=EMAIL,
    python_requires=REQUIRES_PYTHON,
    url=URL,
    install_requires=[
        # 'numpy>=1.16.2',
        # 'opencv-python>=3.0.0'
    ],
    extras_require={
        'pyrender': pyrender_reqs,
        'open3d': open3d_reqs,
        'matplotlib': matplotlib_reqs,
        'all': pyrender_reqs + matplotlib_reqs + open3d_reqs
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        # "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=['pyvlib', 'pyvlib.cv', 'pyvlib.cg']
)
