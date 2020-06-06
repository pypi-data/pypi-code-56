from setuptools import setup, find_packages
from codecs import open
from os import path

current_path = path.abspath(path.dirname(__file__))

with open(path.join(current_path, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()


setup(
    name='amazon_advertising',
    version='1.0.3',
    description='simple Amazon Advertising API client',
    long_description=long_description,
    url='https://gitlab.com/ketu.lai/amazon-advertising',
    author='ketu.lai',
    author_email='ketu.lai@gmail.com',
    license='MIT',
    keywords='amazon advertising api',
    packages=find_packages(),
    install_requires=[],
    tests_require=[],
    python_requires='>=3.6',
)
