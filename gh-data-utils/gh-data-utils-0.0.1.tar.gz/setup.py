import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="gh-data-utils",
    version="0.0.1",
    author="Greenhouse Data Science Team",
    author_email="data-team@greenhouse.io",
    description="A set of utilities for running and evaluating experiments at Greenhouse. Primarily designed to install in a Mode Analytics Python notebook.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/grnhse/gh-data-utils",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
