import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="discogs-api",
    version="0.0.1",
    author="George Rawlinson",
    author_email="george@rawlinson.net.nz",
    description="Python interface to the Discogs API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/grawlinson/python-discogs",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
