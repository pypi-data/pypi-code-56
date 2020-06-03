from setuptools import setup
from os import path
with open(path.join(path.abspath(path.dirname(__file__)), 'README.md'), encoding='utf-8') as f:
    readme_description = f.read()
setup(
name = "foldercheck",
packages = ["foldercheck"],
version = "1.2.1",
license = "MIT",
description = "Don't let your folders keep junk files! FolderCheck lets you review each file in the folder for you to decide wether you want to delete it or not!",
author = "Anime no Sekai",
author_email = "niichannomail@gmail.com",
url = "https://github.com/Animenosekai/python_folderchecker",
download_url = "https://github.com/Animenosekai/python_folderchecker/archive/v1.2.1.tar.gz",
keywords = ['folder', 'check', 'review', 'file', 'management', 'organize'],
install_requires = ['lifeeasy'],
classifiers = ['Development Status :: 4 - Beta', 'License :: OSI Approved :: MIT License', 'Programming Language :: Python :: 3', 'Programming Language :: Python :: 3.4', 'Programming Language :: Python :: 3.5', 'Programming Language :: Python :: 3.6', 'Programming Language :: Python :: 3.7', 'Programming Language :: Python :: 3.8'],
long_description = readme_description,
long_description_content_type = "text/markdown",
entry_points = {'console_scripts': ['foldercheck=foldercheck.command_line:main']}
)
