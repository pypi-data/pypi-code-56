
import os
import setuptools

with open( os.path.join( os.path.dirname( __file__ ),  "README.md" ), "r" ) as fh:
    long_description = fh.read()

setuptools.setup(
    name="spiffyline",
    version="1.0",
    author="Caleb Loera",
    description="Spiff up your CLI with color, formatting, and utilities",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/snakeyworm/spiffyline",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Environment :: Console",
    ],
    python_requires=">=3.6"
)
