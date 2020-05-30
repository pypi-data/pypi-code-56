# -*- coding: utf-8 -*-

import os

from setuptools import setup, find_packages
from shutil import copy2

setup_args = {
    'name': 'ndx-spectrum',
    'version': '0.2.2',
    'description': 'data type for holding power or phase spectra for a signal',
    'author': 'Ben Dichter',
    'author_email': 'ben.dichter@gmail.com',
    'url': '',
    'license': '',
    'install_requires': [
        'pynwb',
        'matplotlib'
    ],
    'packages': find_packages('src/pynwb'),
    'package_dir': {'': 'src/pynwb'},
    'package_data': {'ndx_spectrum': [
        'spec/ndx-spectrum.namespace.yaml',
        'spec/ndx-spectrum.extensions.yaml',
    ]},
    'classifiers': [
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
    ],
    'zip_safe': False
}


def _copy_spec_files(project_dir):
    ns_path = os.path.join(project_dir, 'spec', 'ndx-spectrum.namespace.yaml')
    ext_path = os.path.join(project_dir, 'spec', 'ndx-spectrum.extensions.yaml')

    dst_dir = os.path.join(project_dir, 'src', 'pynwb', 'ndx_spectrum', 'spec')
    if not os.path.exists(dst_dir):
        os.mkdir(dst_dir)

    copy2(ns_path, dst_dir)
    copy2(ext_path, dst_dir)


if __name__ == '__main__':
    _copy_spec_files(os.path.dirname(__file__))
    setup(**setup_args)
