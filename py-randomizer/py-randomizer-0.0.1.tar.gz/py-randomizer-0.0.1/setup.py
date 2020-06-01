import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="py-randomizer",
    version="0.0.1",
    author="Jessica Peck",
    author_email="jessypeck@gmail.com",
    description="A small library that simplifies randomly selecting things from lists.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jessypeck/randomizer",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)