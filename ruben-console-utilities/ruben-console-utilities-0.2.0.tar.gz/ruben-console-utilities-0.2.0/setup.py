import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ruben-console-utilities",
    version="0.2.0",
    author="Ruben Dougall",
    # author_email="author@example.com",
    description="Simple utility functions for command-line applications.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Ruben9922/python-console-utilities",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
