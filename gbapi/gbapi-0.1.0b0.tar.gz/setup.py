import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="gbapi", # Replace with your own username
    version="0.1.0b",
    author="qeaml",
    author_email="qeaml@wp.pl",
    description="qeaml's wrapper for GameBanana's API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/QeaML/gbapi",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)