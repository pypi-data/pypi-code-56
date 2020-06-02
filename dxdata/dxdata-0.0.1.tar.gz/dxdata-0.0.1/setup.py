import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="dxdata", # Replace with your own username
    version="0.0.1",
    author="DNAnexus, Inc.",
    author_email="dnanexus@dnanexus.com",
    description="",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dnanexus/dx-toolkit",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=2.7',
)
