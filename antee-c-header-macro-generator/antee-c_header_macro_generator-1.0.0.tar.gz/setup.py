from setuptools import (
    setup,
    find_namespace_packages
)


with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="antee-c_header_macro_generator",
    version="1.0.0",
    author="Yi Zhang",
    author_email="zhangyiant@hotmail.com",
    description="C header macro name generator",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/zhangyiant/c_header_macro_generator",
    package_dir={'': 'src'},
    packages=find_namespace_packages(
        where="src"
    ),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
