#!/usr/bin/env python
from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="sentry-dingtalk-robot",
    version='0.0.1',
    author='loopbless',
    author_email='243917133@qq.com',
    url='https://github.com/loopbless/sentry-dingding',
    description='A Sentry extension which integrates with Dinttalk robot.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    license='MIT',
    keywords='sentry dingding dingtalk',
    package_dir={'': 'src'},
    packages=find_packages('src'),
    install_requires=[
        'sentry>=9.0.0',
        'requests',
    ],
    entry_points={
        'sentry.plugins': [
            'sentry_dingtalk_robot = sentry_dingtalk_robot.plugin:DingTalkPlugin'
        ]
    },
    classifiers=[
        'Programming Language :: Python :: 2.7',
        "License :: OSI Approved :: MIT License",
    ]
)
