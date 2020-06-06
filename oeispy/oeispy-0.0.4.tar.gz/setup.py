from setuptools import setup,find_packages
from os import path

long_description=''
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

classifiers=['Development Status :: 4 - Beta',
             'Intended Audience :: Education',
             'Operating System :: Microsoft :: Windows :: Windows 10',
             'License :: OSI Approved :: MIT License',
             'Programming Language :: Python :: 3']

setup(
    name='oeispy',
    version='0.0.4',
    description='Simple Python Library for OEIS',
    long_description_content_type='text/markdown',
    long_description=long_description+'\n\n'+open('CHANGELOG.txt').read(),
    url='https://github.com/phantom-5/oeispy',
    author='Rudra M Biswal',
    author_email='rickrudra@gmail.com',
    license='MIT',
    classifiers=classifiers,
    keywords='oeis',
    packages=find_packages(),
    install_requires=['requests']


)