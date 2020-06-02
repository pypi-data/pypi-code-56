from setuptools import setup
from os import path
with open(path.join(path.abspath(path.dirname(__file__)), 'README.md'), encoding='utf-8') as f:
    readme_description = f.read()
setup(
name = "packageupload",
packages = ["packageupload"],
version = "0.1",
license = "MIT",
description = "The most easy way to upload your packages to PyPI",
author = "Anime no Sekai",
author_email = "niichannomail@gmail.com",
url = "https://github.com/Animenosekai/packageupload",
download_url = "https://github.com/Animenosekai/packageupload/archive/0.1.tar.gz",
keywords = ['upload', 'package', 'pip', 'pypi', 'packageupload', 'pypiupload'],
install_requires = ['setuptools', 'filecenter', 'lifeeasy', 'twine'],
classifiers = ['Development Status :: 4 - Beta', 'License :: OSI Approved :: MIT License', 'Programming Language :: Python :: 3', 'Programming Language :: Python :: 3.4', 'Programming Language :: Python :: 3.5', 'Programming Language :: Python :: 3.6', 'Programming Language :: Python :: 3.7', 'Programming Language :: Python :: 3.8'],
long_description = readme_description,
long_description_content_type = "text/markdown"
)
