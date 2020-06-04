# encoding: utf-8
# Author: gdream@126.com
from setuptools import setup, find_packages


with open("README.md", "r", encoding="utf-8") as f:
    descriptions = f.read()

setup(
    name='fontencrypt',
    version='0.1.0',
    author='gdream@126.com',
    description='一个由Python实现的字体加密库(反爬)',
    long_description=descriptions,
    long_description_content_type="text/markdown",
    url='https://github.com/ggdream/fontencrypt',
    packages=find_packages(),
    install_requires=['fonttools>=4.0.0']
)
