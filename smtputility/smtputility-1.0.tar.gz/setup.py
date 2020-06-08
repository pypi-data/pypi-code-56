from setuptools import setup, Extension, find_packages
from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="smtputility",
    packages=['smtputility'],
    version="1.0",
    author="Matthew Jensen",
    author_email="matt@matthewjensen.dev",
    description="SMTP email automation functions",
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/MattDJensen/SMTP_Utility_Package',
    download_url='https://github.com/MattDJensen/SMTP_Utility_Package/archive/1.0.tar.gz',
    license="MIT",
    setup_requires=['wheel'],
    install_requires=[
    ],
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Operating System :: OS Independent"
    ],
    python_requires='>=3.6',
)
