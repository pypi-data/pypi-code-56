import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ulaumwencien-hello32",
    version="2.0",
    author="ulaumwencien",
    author_email="UNKNOWN",
    description="UNKNOWN",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="UNKNOWN",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
