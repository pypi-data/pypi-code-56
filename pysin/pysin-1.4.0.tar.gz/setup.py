import os
from setuptools import setup, find_packages

with open(
    os.path.join(os.path.abspath(os.path.dirname(__file__)), "README.md"), encoding="utf-8",
) as f:
    long_description = f.read()


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


requirements = read("requirements.txt").split()

setup(
    name="pysin",
    packages=find_packages(),
    include_package_data=True,
    entry_points={
        "console_scripts": [
            "pysin-gen-db=pysin.mimic.cli:generate_database",
            "pysin-gen-pdf=pysin.mimic.cli:generate_pdf",
            "pysin-preprocess=pysin.mimic.cli:preprocess",
            "pysin-scrap=pysin.mimic.cli:scrap",
        ]
    },
    version="1.4.0",
    license="Apache License 2.0",
    description="PySin is a toolbox for text retrieval in unstructured documents datasets. It contains both a multi-type text extractor and a search engine. To test them, you can use the medical prescriptions generator that is also provided.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Jean-Baptiste Laval",
    author_email="contact@arkhn.com",
    url="https://github.com/arkhn/PySin",
    download_url="https://github.com/arkhn/PySin/archive/1.1.0.tar.gz",
    keywords=[
        "arkhn",
        "text retrieval",
        "search engine",
        "text extraction",
        "dataset generator",
        "medical",
    ],
    install_requires=requirements,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
)
