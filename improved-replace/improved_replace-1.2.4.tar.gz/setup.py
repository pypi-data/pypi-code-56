#!/usr/bin/python3
from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="improved_replace",
    version="1.2.4",
    description="Add replace method improvements",
    url="https://github.com/LuckJMG/ImprovedReplace",
    author="LuckJMG",
    author_email="lucas.mosquera13@gmail.com",
    license="MIT license",
    long_description=long_description,
    platforms="OS Independent",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    long_description_content_type="text/markdown",
    packages=find_packages(exclude=["tests"]),
)
