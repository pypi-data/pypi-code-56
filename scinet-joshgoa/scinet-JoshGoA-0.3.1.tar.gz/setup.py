import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="scinet-JoshGoA",
    version="0.3.1",
    author="JoshGoA",
    description="Network science abstract data types",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/JoshGoA/scinet.git",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)
