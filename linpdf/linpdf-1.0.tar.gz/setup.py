import setuptools 

from pathlib import Path

setuptools.setup(
    name="linpdf",
    version=1.0,
    long_Description=Path("README.md").read_text(),
    packages=setuptools.find_packages(exclude=["tests", "data"])
)