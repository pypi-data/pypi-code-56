import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

DOCLINES = (__doc__ or '').split("\n")

setuptools.setup(
    name="pycommerce",
    version="0.0.1",
    author="Joridos",
    description=DOCLINES[0],
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pycommerce/pycommerce",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)
