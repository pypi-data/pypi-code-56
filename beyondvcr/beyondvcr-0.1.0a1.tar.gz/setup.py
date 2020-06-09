#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open("README.rst") as readme_file:
    readme = readme_file.read()

with open("HISTORY.rst") as history_file:
    history = history_file.read()

requirements = [
    'requests'
]

setup_requirements = [ ]

test_requirements = []

setup(
    author="Elias Dorneles",
    author_email="eliasdorneles@gmail.com",
    python_requires=">=3.5",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    description="BeyondVCR helps you to write tests for code that does HTTP calls",
    install_requires=requirements,
    license="MIT license",
    long_description=readme + "\n\n" + history,
    include_package_data=True,
    keywords="beyondvcr",
    name="beyondvcr",
    packages=find_packages(include=["beyondvcr", "beyondvcr.*"]),
    setup_requires=setup_requirements,
    test_suite="tests",
    tests_require=test_requirements,
    url="https://gitlab.com/eliasdorneles/beyondvcr",
    version="0.1.0a1",
    zip_safe=False,
)
