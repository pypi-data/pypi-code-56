from setuptools import setup, find_packages

with open("README.md","r") as fh:
    long_desc = fh.read()


setup(
    name="DBS-MAIA",
    version="0.0",
    author="MAIA",
    long_description=long_desc,
    long_description_content_type="text/markdown",
    url="",
    license="Apache Software License (Apache License 2.0)",
    packages=find_packages(),
    python_requires=">=3.6",
    scripts=[],
    include_package_data=True,
    zip_safe=False
)
