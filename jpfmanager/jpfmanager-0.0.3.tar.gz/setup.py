import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="jpfmanager",
    version="0.0.3",
    author="Ibrahim Abbas",
    author_email="i.abbas85@gmail.com",
    description="File manager to deal with json and pickle files",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/IbrahimABBAS85/jpf",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        "pathlib",
        "jsonpickle"
    ],
)
