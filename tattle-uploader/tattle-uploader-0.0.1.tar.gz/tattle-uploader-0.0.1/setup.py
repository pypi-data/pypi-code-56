import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="tattle-uploader",
    version="0.0.1",
    description="Helper functions to assist tattle services in storing data",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/tattle-made/",
    author="kruttikanadig",
    author_email="kruttika@tattle.co.in",
    license="GPL-3",
    packages=["uploader"],
    include_package_data=True,
    install_requires=["boto3", "pymongo"],
    entry_points={
        "console_scripts": [
            "realpython=reader.__main__:main",
        ]
    },
)
