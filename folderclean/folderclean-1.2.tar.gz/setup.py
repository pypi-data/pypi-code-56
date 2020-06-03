from setuptools import setup
from os import path
with open(path.join(path.abspath(path.dirname(__file__)), 'README.md'), encoding='utf-8') as f:
    readme_description = f.read()
setup(
name = "folderclean",
packages = ["folderclean"],
version = "1.2",
license = "MIT",
description = "Clean your folders in a single line of code! FolderCleans lets you for example clean your folders and organize them by file types.",
author = "Anime no Sekai",
author_email = "niichannomail@gmail.com",
url = "https://github.com/Animenosekai/folder_cleaner",
download_url = "https://github.com/Animenosekai/folder_cleaner/archive/v1.2.tar.gz",
keywords = ['clean', 'folder', 'directory', 'cleaning', 'folderclean', 'animenosekai', 'sort', 'filecenter', 'lifeeasy'],
install_requires = ['filecenter', 'lifeeasy'],
classifiers = ['Development Status :: 4 - Beta', 'License :: OSI Approved :: MIT License', 'Programming Language :: Python :: 3', 'Programming Language :: Python :: 3.4', 'Programming Language :: Python :: 3.5', 'Programming Language :: Python :: 3.6', 'Programming Language :: Python :: 3.7', 'Programming Language :: Python :: 3.8'],
long_description = readme_description,
long_description_content_type = "text/markdown",
entry_points = {'console_scripts': ['folderclean=folderclean.command_line:main']}
)
