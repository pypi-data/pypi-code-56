import setuptools
from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="makecmd",
    version=1.8,
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    install_requires=['argparse'],
    entry_points={'console_scripts': ['makecmd = makecmd.makecmd:main']}
)
