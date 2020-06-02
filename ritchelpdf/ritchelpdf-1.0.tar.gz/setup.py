import setuptools
from pathlib import Path


setuptools.setup(
    name="ritchelpdf",             # should be unique within pypi community projects
    version=1.0,
    long_description=Path("README.md").read_text(),
    packages=setuptools.find_packages(exclude=["test", "data"])
)
