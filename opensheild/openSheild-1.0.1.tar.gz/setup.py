import setuptools
from setuptools import setup,find_packages
import os


with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="openSheild", # Replace with your own username
    version="1.0.1",
    author="Dejun E",
    author_email="edj17@lzu.edu.cn",
    description="The module of post-processing MCNP output file",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)