#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from __future__ import absolute_import
from __future__ import print_function

import io
import re
from glob import glob
from os.path import basename
from os.path import dirname
from os.path import join
from os.path import splitext

from setuptools import find_packages
from setuptools import setup


def read(*names, **kwargs):
    with io.open(
        join(dirname(__file__), *names),
        encoding=kwargs.get('encoding', 'utf8')
    ) as fh:
        return fh.read()


setup(
    name='dvg-qdeviceio',
    version='0.0.1',
    license='MIT',
    description='PyQt5 framework for multithreaded communication and periodical data acquisition for an I/O device.',
    long_description='%s\n%s' % (
        re.compile('^.. start-badges.*^.. end-badges', re.M | re.S).sub('', read('README.md')),
        re.sub(':[a-z]+:`~?(.*?)`', r'``\1``', read('CHANGELOG.md'))
    ),
    long_description_content_type='text/markdown',
    author='Dennis van Gils',
    author_email='vangils.dennis@gmail.com',
    url='https://github.com/Dennis-van-Gils/python-dvg-qdeviceio',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    py_modules=[splitext(basename(path))[0] for path in glob('src/*.py')],
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        # complete classifier list: http://pypi.python.org/pypi?%3Aaction=list_classifiers
        #'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Scientific/Engineering :: Electronic Design Automation (EDA)',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        # uncomment if you test on these interpreters:
        # 'Programming Language :: Python :: Implementation :: IronPython',
        # 'Programming Language :: Python :: Implementation :: Jython',
        # 'Programming Language :: Python :: Implementation :: Stackless',
    ],
    project_urls={
        'Issue Tracker': 'https://github.com/Dennis-van-Gils/python-dvg-qdeviceio/issues',
    },
    keywords=[
        # eg: 'keyword1', 'keyword2', 'keyword3',
        'PyQt5', 'multithread', 'device I/O', 'automation', 'laboratory', 'science',
    ],
    python_requires='>=3.5',
    install_requires=[
        # eg: 'aspectlib==1.1.1', 'six>=1.7',
        'pyqt5>=5.9.2,<6',
        'numpy>=1.16.4,<2',
        'dvg-debug-functions>=1.0.1',
    ],
    extras_require={
        'dev': [
            'pytest-cov',
        ]
        # eg:
        #   'rst': ['docutils>=0.11'],
        #   ':python_version=="2.6"': ['argparse'],
    },
)
