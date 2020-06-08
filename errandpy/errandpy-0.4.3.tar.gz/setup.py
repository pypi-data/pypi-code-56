import setuptools

from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding="utf-8") as f:
    description = f.read()

setuptools.setup(
    name="errandpy",
    version="0.4.3",
    description="an automatical tool for extracting short-range force in NC-AFM data",
    author="ZHUO DIAO",
    author_email="enzian0515@gmail.com",
    license="MIT",
    packages=setuptools.find_packages(),
    long_description=description,
    long_description_content_type="text/markdown",
    include_package_data=True,
    install_requires=["tensorflow==1.12.0", "matplotlib"]
)