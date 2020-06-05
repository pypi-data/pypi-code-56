# coding: utf-8

import setuptools

setuptools.setup(
    name="nihao",
    version="0.1.1",
    author="蔡炜桀",
    author_email="justcoding@qq.com",
    description="中文识别包",
    long_description=open('README.md', encoding='utf-8').read(),
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