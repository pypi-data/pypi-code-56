import os
import setuptools

local_requirements = 'requirements.txt'

with open("README.md", "r") as fh:
        long_description = fh.read()

lines = []
if os.path.exists(local_requirements):
    with open(local_requirements, 'r') as f:
      lines = f.read().split('\n')

requirements = [package for package in lines if package and not package.startswith('#')]


setuptools.setup(
    name="phoenix-cli",
    version="0.0.2",
    license="MIT",
    author="Pitsanu Swangpheaw",
    author_email="pitsanu_s@hotmail.com",
    description="Phoenix Command Line Interface",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://pypi.org/project/phoenix-cli/",
    packages=setuptools.find_packages(),
    install_requires=requirements,
    python_requires=">=3.6",
    scripts=["px"]
)

