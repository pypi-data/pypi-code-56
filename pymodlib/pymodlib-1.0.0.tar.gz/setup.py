#!/usr/bin/env python
# coding: utf-8
# In[32]:
import setuptools
with open("README.md", "r") as fh:
    long_description = fh.read()
setuptools.setup(
    name="pymodlib", # Replace with your own username
    version="1.0.0",
    author="Ignacio Juica",
    author_email="electric.sspa@gmail.com",
    description="Modbus Server for PLC Siemens LOGO8",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ignaciojuica/PyMod",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)

