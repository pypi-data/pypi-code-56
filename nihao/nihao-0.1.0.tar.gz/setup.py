# coding: utf-8

import setuptools

with open("README.md", "rb") as fh:
    long_description = fh.read()
    long_description = long_description.decode(encoding='utf-8')

setuptools.setup(
    name="nihao",
    version="0.1.0",
    author="蔡炜桀",
    author_email="justcoding@qq.com",
    description="中文识别",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/czcaiwj/chinese",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)