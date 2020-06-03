from setuptools import setup
from os import path
with open(path.join(path.abspath(path.dirname(__file__)), 'README.md'), encoding='utf-8') as f:
    readme_description = f.read()
setup(
name = "packageupload",
packages = ["packageupload"],
version = "1.5.1",
license = "MIT",
description = "The most easy way to upload your packages to PyPI!",
author = "Anime no Sekai",
author_email = "niichannomail@gmail.com",
url = "https://github.com/Animenosekai/packageupload",
download_url = "https://github.com/Animenosekai/packageupload/archive/v1.3.tar.gz",
keywords = ['package', 'packageupload', 'upload', 'pip', 'pypi', 'pypiupload', 'animenosekai', 'python'],
install_requires = ['setuptools', 'twine', 'lifeeasy', 'filecenter'],
classifiers = ['Development Status :: 4 - Beta', 'License :: OSI Approved :: MIT License', 'Programming Language :: Python :: 3', 'Programming Language :: Python :: 3.4', 'Programming Language :: Python :: 3.5', 'Programming Language :: Python :: 3.6', 'Programming Language :: Python :: 3.7', 'Programming Language :: Python :: 3.8'],
long_description = readme_description,
long_description_content_type = "text/markdown",
entry_points = {'console_scripts': ['packageupload=packageupload.command_line:main']}
)
