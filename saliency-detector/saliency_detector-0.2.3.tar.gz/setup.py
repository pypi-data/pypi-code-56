#!/usr/bin/env python
"""The setup script."""

import re
from pathlib import Path
from setuptools import setup, find_packages


def find_version(fname):
    """Attempt to find the version number in the file fname.
    Raises RuntimeError if not found.
    """
    version = ""
    reg = re.compile(r'__version__ = [\'"]([^\'"]*)[\'"]')
    for line in Path(fname).read_text().split("\n"):
        m = reg.match(line)
        if m:
            version = m.group(1)
            break
    if not version:
        raise RuntimeError("Cannot find version information")
    return version


with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = ['torch',
                'torchvision',
                'scipy',
                'pillow',
                'opencv-python']

setup(
    author="Adam Dudley Lewis",
    author_email='balast@users.noreply.github.com',
    python_requires='>=3.5',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        "Operating System :: OS Independent",
    ],
    description="Pretrained Poolnet Saliency Detector for Inference",
    install_requires=requirements,
    license="GNU General Public License v3",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='saliency_detector',
    name='saliency_detector',
    packages=find_packages(include=['saliency_detector', 'saliency_detector.*']),
    test_suite='tests',
    url='https://github.com/balast/saliency_detector',
    version=find_version('saliency_detector/__init__.py'),
    zip_safe=False,
)
