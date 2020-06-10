# Copyright (c) 2018 WeFindX Foundation, CLG.
# All Rights Reserved.

from setuptools import find_packages, setup

setup(
    name='0rss',
    version='0.0.0',
    description='Trying something.',
    url='https://github.com/mindey/0rss',
    author='Mindey',
    author_email='mindey@qq.com',
    license='MIT',
    packages = find_packages(exclude=['docs', 'tests*']),
    install_requires=[
        'metaform',
        'metatype',
    ],
    extras_require = {
        'test': ['coverage', 'pytest', 'pytest-cov'],
    },
    zip_safe=False,
    entry_points = {
        'console_scripts': [
        ],
    }
)
