"""Setup script."""

import os
import pathlib
import re

from setuptools import setup, find_packages

# Set the environment variable TF_CPU (to anything) to use tensorflow-cpu
_TF_CPU = os.environ.get('TF_CPU', None)

# TensorFlow package name and version
_TF = 'tensorflow' if _TF_CPU is None else 'tensorflow-cpu'
_MIN_TF_VERSION = '2.2'
_TF += f'>={_MIN_TF_VERSION}'

# Directory of this setup.py file
_HERE = pathlib.Path(__file__).parent


def _resolve_path(*parts):
    """Get a filename from a list of path components, relative to this file."""
    return _HERE.joinpath(*parts).absolute()


def _read(*parts):
    """Read a file's contents into a string."""
    filename = _resolve_path(*parts)
    return filename.read_text()


__INIT__ = _read('src', 'trainable_initial_state_rnn', '__init__.py')


def _get_package_variable(name):
    pattern = rf'^{name} = [\'"](?P<value>[^\'"]*)[\'"]'
    match = re.search(pattern, __INIT__, flags=re.M)
    if match:
        return match.group('value')
    raise RuntimeError(f'Cannot find variable {name}')


setup(
    name=_get_package_variable('__package__'),
    version=_get_package_variable('__version__'),
    description=_get_package_variable('__description__'),
    url=_get_package_variable('__url__'),
    author=_get_package_variable('__author__'),
    author_email=_get_package_variable('__author_email__'),
    long_description=_read('README.rst'),
    long_description_content_type='text/x-rst',
    packages=find_packages('src', exclude=['*.tests']),
    package_dir={'': 'src'},
    license='Apache 2.0',
    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'Topic :: Scientific/Engineering :: Mathematics',
        'Topic :: Software Development',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    install_requires=[
        _TF,
    ],
    extras_require={
        # The 'dev' extra is for development, including running tests and
        # generating documentation
        'dev': [
            'numpy',
            'pytest',
            'coverage',
            'sphinx',
            'sphinx_rtd_theme',
        ],
    },
    zip_safe=False,
)
