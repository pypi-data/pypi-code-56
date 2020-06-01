# -*- coding:utf-8 -*-
# @author :adolf
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="rpa_ocr",
    version="0.0.5",
    author="adolf",
    author_email="adolf1321794021@gmail.com",
    description="A Tools for use algorithm for verification recognition",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://code.ii-ai.tech/zhutaonan/rpa_verification.git",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
