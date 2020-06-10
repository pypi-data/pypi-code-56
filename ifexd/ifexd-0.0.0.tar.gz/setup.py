import setuptools
import os

with open("README.md", "r") as fh:
    long_description = fh.read()

top_dir, _ = os.path.split(os.path.abspath(__file__))

with open(os.path.join(top_dir, 'Version')) as f:
    version = f.readline().strip()

setuptools.setup(
    name="ifexd",
    version= version,
    author="Nikesh Bajaj",
    author_email="nikkeshbajaj@gmail.com",
    description="IFExD: Indian Facial Expression Dataset",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Nikeshbajaj/ifexd",
    packages=setuptools.find_packages(),
    license = 'MIT',
    keywords = 'Facial-Expression-Dataset Computer-Vision CNN',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    include_package_data=True,
    install_requires=['numpy','matplotlib','spkit']
)
