from setuptools import setup, Extension, find_packages
from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="outlookutility",
    packages=['outlookutility'],
    version="1.0",
    author="Matthew Jensen",
    author_email="matt@matthewjensen.dev",
    description="Outlook email automation functions",
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/MattDJensen/Outlook_Utility_Package',
    download_url='https://github.com/MattDJensen/Outlook_Utility_Package/archive/1.0.tar.gz',
    license="MIT",
    setup_requires=['wheel'],
    install_requires=[
        'pywin32'
    ],
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Operating System :: Microsoft :: Windows :: Windows 10"
    ],
    python_requires='>=3.6',
)
