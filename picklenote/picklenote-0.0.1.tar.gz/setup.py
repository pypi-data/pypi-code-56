import setuptools

from picklenote import __version__

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="picklenote",
    version=__version__,
    author="Kent Kawashima",
    author_email="kentkawashima@gmail.com",
    description="Pickle an object together with a short note about it",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kentwait/picklenote",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Utilities",
    ],
    python_requires='>=3.6',
)
