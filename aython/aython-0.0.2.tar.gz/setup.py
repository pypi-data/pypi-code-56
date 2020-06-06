import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="aython",
    version="0.0.2",
    author="Edward Wildman",
    description="A small easy to use tool for building alexa apps with python",
    long_description="text/markdown",
    long_description_content_type="text/markdown",
    url="https://github.com/wedwrd/aython",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    ],
    python_requires='>=3.6',
)
