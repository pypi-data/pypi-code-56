import os
from setuptools import setup, find_packages

def readme():
    with open('README.md') as f:
        return f.read()

PACKAGE_NAME = 'ha-philipsjs-rik'
HERE = os.path.abspath(os.path.dirname(__file__))
VERSION = '0.0.91'

PACKAGES = find_packages(exclude=['tests', 'tests.*', 'dist', 'ccu', 'build'])

REQUIRES = []

setup(
        name=PACKAGE_NAME,
        version=VERSION,
        license='MIT License',
        url='https://github.com/rikbruggink/ha-philipsjs',
        download_url='https://github.com/rikbruggink/ha-philipsjs/tarball/'+VERSION,
        author='Rik Bruggink',
        author_email='mail@rikbruggink.nl',
        description='jointSPACE API for Home-Assistant',
        packages=PACKAGES,
        include_package_data=True,
        zip_safe=False,
        platforms='any',
        install_requires=REQUIRES,
        keywords=['jointSPACE'],
        classifiers=[
            'Intended Audience :: Developers',
            'License :: OSI Approved :: MIT License',
            'Operating System :: OS Independent',
            'Programming Language :: Python :: 3.4'
        ],
        extras_require={
            'tests': [
                'pytest>3.6.4',
                'pytest-requests',
                'pytest-cov<2.6',
                'coveralls',
                'pytest-mock',
            ]
        },
)
