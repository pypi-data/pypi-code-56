from setuptools import setup, find_packages
from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="gsuite",
    version="1.0.0",
    packages=find_packages(),
    url="https://github.com/traveloka/gsuite-python-library",
    license="Apache License 2.0",
    author="Rafi Kurnia Putra",
    author_email="rafi.putra@traveloka.com",
    description="Python library to interact with Google Suite API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=["google-api-python-client==1.8.0", "google-auth-oauthlib==0.4.1"],
    python_requires=">=3",
)
