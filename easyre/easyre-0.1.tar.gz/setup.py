# coding=utf-8

from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='easyre',

    version="0.1",
    description=(
        'A Reg XBag'

    ),
    long_description=open('README.md', 'r').read(),
    long_description_content_type="text/markdown",
    author='felix',
    author_email='felix2@foxmail.com',
    maintainer='felix',
    maintainer_email='felix2@foxmail.com',
    license='MIT License',
    packages=["easyre"],

    url='https://github.com/xiezheyuan/easyre/',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: Implementation',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries'
    ],

)

