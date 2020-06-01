import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="crossref_commons_reverse",
    version="0.0.7.1",
    author="Lukas Barth",
    author_email="pypi@mbox.tinloaf.de",
    description="Crossref Commons with added Reverse-Search",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/tinloaf/crossref_commons_py",
    install_requires=["ratelimit >= 2.2.1", "requests >= 2.18.4"],
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
