import setuptools
from odia import __version__


with open("README.md", "r") as fh:
    long_description = fh.read()



setuptools.setup(
    name="odia", # Replace with your own username
    version=__version__,
    author="Biranchi Narayan Nayak",
    author_email="biranchi125@gmail.com",
    description="Odia language",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/biranchi2018/odia",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
