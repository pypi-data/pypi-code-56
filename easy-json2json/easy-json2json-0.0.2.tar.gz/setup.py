import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="easy-json2json",
    version="0.0.2",
    author="brworkit",
    author_email="brworkit@gmail.com",
    description="A package for easy json parse.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/brworkit/python-package-easy-json2json.git",
    download_url = 'https://github.com/brworkit/python-package-easy-json2json/archive/v0.0.2.tar.gz',    # I explain this later on
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)