import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="bimp", # Replace with your own username
    version="1.7",
    author="Jan Smejkal",
    author_email="jankosmejkal@yahoo.com",
    description="Make-life-easier Python functions for image processing.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/JankoSmejkal/bimp/blob/master/README.md",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)

