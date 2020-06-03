import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path("/Users/dogukangundogan/PycharmProjects/DomOdev2")

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="XmlCsvJsonConvert",
    version="1.1.2",
    description="File convert for xml csv or json ",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/DogukanGun/FileConvert",
    author="Dogukan Ali Gundogan",
    author_email="dogukangundogan5@gmail.com",
    license="Dag",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    include_package_data=True,
    install_requires=["Tree","jsonlib-python3"],
    entry_points={
        "console_scripts": [
            "file_convertor=reader.__main__:main",
        ]
    },
    setup_requires=['wheel']
)
