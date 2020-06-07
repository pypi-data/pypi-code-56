import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

REQUIRES = [
    "requests",
    "bs4",
    "lxml"
]

setuptools.setup(
    name="downloadimages",
    version="0.0.1",
    author="diepthuyhan",
    author_email="",
    description="Get image url from a few website",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/diepthuyhan/downloadImages",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
