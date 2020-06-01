import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="aricma_pretty_print",  # Replace with your own username
    version="0.0.2",
    author="Adrian Mindak",
    description="A small printer package "
                "to get some better looking print statements for any cli.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/aricma/pretty-print.git",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)