import setuptools
from setuptools import find_packages


with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="xpi_blocks", 
    version="0.0.18",
    author="Viacheslav Karpizin",
    author_email="karpizin@gmail.com",
    description="Package for xPI boards to handle sensors and peripherial devices",
    #url="https://github.com/xtile/rpi_blocks",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.5',
    zip_safe=False
)
