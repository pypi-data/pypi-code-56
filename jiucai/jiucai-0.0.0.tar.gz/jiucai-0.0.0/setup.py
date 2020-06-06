import setuptools

with open("README.md", "r",encoding='utf8') as fh:
    long_description = fh.read()

setuptools.setup(
    name="jiucai",
    version="0.0.0",
    author="yanyan",
    author_email="shiyanaimama@163.com",
    description="jiucai",
    long_description=long_description,
    long_description_content_type="text/markdown",
    #url="https://github.com/pypa/sampleproject",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)