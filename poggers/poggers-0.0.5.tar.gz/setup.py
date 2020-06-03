import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="poggers", # Replace with your own username
    version="0.0.5",
    author="Rika",
    author_email="jayden05jaydenhigginsjayden05@hotmail.com",
    description="A small package for converting text to ascii",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://google.com",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)