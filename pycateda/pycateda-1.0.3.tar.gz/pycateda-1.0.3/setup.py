import setuptools
import os
import sys
with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pycateda",  # name of package
    version="1.0.3",
    author="Arjun Srinivasa Murthy",
    author_email="arjunsm2020@gmail.com",
    license="MIT",
    description="pycateda Python Package - A simplified Exploratory Data Analysis with less lines of code",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/arjuns2020/pycateda",
    packages=setuptools.find_packages(),
    include_package_data=True,
    install_requires=["matplotlib", "numpy","pandas", "seaborn", "missingno", "notebook","pandas_profiling"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",

    ],
    python_requires='>=3.5',
)
