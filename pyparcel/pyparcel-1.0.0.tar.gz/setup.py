import setuptools
import pyparcel

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name=pyparcel.__title__,
    version=pyparcel.__version__,
    author=pyparcel.__author__,
    author_email=pyparcel.__author_email__,
    description="Easy to use binary packer that doesn't require struct's specifications",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/najaco/pyparcel",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
