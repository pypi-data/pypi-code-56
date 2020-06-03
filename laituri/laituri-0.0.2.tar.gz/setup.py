import ast
import os
import re

import setuptools

with open(os.path.join(os.path.dirname(__file__), 'laituri', '__init__.py')) as infp:
    version = ast.literal_eval(re.search('__version__ = (.+?)$', infp.read(), re.M).group(1))

with open('README.md', 'r') as fp:
    long_description = fp.read()

dev_dependencies = [
    'flake8',
    'isort',
    'pydocstyle',
    'pytest',
    'pytest-cov',
    'pytest-mock',
]

if __name__ == '__main__':
    setuptools.setup(
        name='laituri',
        description='Docker Toolkit for Python',
        long_description=long_description,
        long_description_content_type='text/markdown',
        version=version,
        author='Valohai',
        author_email='hait@valohai.com',
        maintainer='Ruksi Laine',
        maintainer_email='me@ruk.si',
        url='https://github.com/valohai/laituri',
        license='MIT',
        packages=setuptools.find_packages('.', exclude=('laituri_tests', 'laituri_tests.*',)),
        install_requires=[],
        tests_require=dev_dependencies,
        extras_require={'dev': dev_dependencies},
        classifiers=[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
        ],
    )
