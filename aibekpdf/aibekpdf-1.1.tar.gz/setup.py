import setuptools
from pathlib import Path

setuptools.setup(
    name="aibekpdf",
    version=1.1,
    long_decription=Path("README.md").read_text(),
    packages=setuptools.find_packages(exclude=["tests", "data"])
)
