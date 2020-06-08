import setuptools
with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="file_op",
    version="0.0.1",
    author="Arun Jaiswal",
    author_email="arrrsh@gmail.com" ,
    description="Find delimiter for a input file data",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Natural Language :: English"
    ],
    python_requires='>=3.6',
)