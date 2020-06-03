import os
from setuptools import setup, find_packages


with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="femtools", # Replace with your own username
    version="0.0.1",
    author="thaddywu",
    author_email="thaddywu@gmail.com",
    description="Forecast-elicitation-Mechanism",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Hermera/Forecast-elicitation-Mechanism",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)