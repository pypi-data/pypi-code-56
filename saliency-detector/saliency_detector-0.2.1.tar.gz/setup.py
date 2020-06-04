#!/usr/bin/env python
import setuptools

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

# requirements = ['torch',
#                 'torchvision',
#                 'scipy',
#                 'pillow',
#                 'opencv-python']
requirements = []

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
    version='0.2.1',
    zip_safe=False,
)
