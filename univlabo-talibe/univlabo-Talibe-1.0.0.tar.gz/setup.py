from setuptools import find_packages, setup

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="univlabo-Talibe", # Replace with your own username
    version="1.0.0",
    author="Ndate SOW",
    author_email="ndatesowthioune@gmail.com",
    description="A LIBRAIRY",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/SokhnaNdate/univlabo",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)