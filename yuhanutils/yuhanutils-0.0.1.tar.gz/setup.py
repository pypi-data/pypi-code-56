from setuptools import setup, find_packages

with open("README.md", 'r') as fh:
    long_description = fh.read()

setup(
    name='yuhanutils',
    version='0.0.1',
    author='Yuhan Chen',
    author_email='chenyh@umich.edu',
    description="Some useful utilities put together by Yuhan Chen",
    long_description=long_description,
    packages=find_packages(),
)
