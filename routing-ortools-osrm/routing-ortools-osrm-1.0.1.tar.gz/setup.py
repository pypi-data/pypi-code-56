import pathlib

from setuptools import find_packages, setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="routing-ortools-osrm",
    version="1.0.1",
    description="Package to use Ortools combine with Osrm for routing",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/Tonow/routing-ortools-osrm",
    author="Thomas Nowicki",
    author_email="thomas.nowicki@camptocamp.com",
    license="Apache 2.0",
    classifiers=[
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=find_packages(exclude=("tests",)),
    include_package_data=True,
    install_requires=[
        "ortools",
        "gdal==2.2",
        "pynominatim",
        "osrm",
        "matplotlib==2.2.4",
    ],
    python_requires=">=3.6",
)
