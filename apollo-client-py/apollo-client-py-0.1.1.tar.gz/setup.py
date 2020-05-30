# encoding: utf-8
from setuptools import setup, find_packages

SHORT = 'a client for apollo - fix'

__version__ = "0.1.1"
__author__ = 'RedButterfly'
__email__ = 'hanfei1009@126.com'
readme_path = 'README.md'

setup(
    name='apollo-client-py',
    version=__version__,
    packages=find_packages(),
    install_requires=[
        'requests', 'eventlet'
    ],
    url='https://github.com/red-butterfly/pyapollo',
    author=__author__,
    author_email=__email__,
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 2.7',
    ],
    include_package_data=True,
    package_data={'': ['*.py', '*.pyc']},
    zip_safe=False,
    platforms='any',

    description=SHORT,
    long_description=open(readme_path, encoding='utf-8').read(),
    long_description_content_type='text/markdown',
)
