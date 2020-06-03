import setuptools

with open("README.md", "r") as f:
    long_description = f.read()

setuptools.setup(
    name="atompack",
    version="0.1.0",
    author="Seaton Ullberg",
    author_email="seatonullberg@gmail.com",
    description="A flexible Python library for atomic structure generation",
    long_description=long_description,
    long_description_content="text/markdown",
    url="https://github.com/seatonullberg/atompack",
    packages=setuptools.find_packages(),
    license="MIT",
    install_requires=["numpy", "scipy"],
)
