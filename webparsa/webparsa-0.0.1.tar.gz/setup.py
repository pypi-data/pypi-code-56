import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()
    
setuptools.setup(
    name="webparsa",
    version="0.0.1",
    author="Michael Fatemi",
    author_email="myfatemi04@gmail.com",
    description="This project uses XML templates to extract data from websites for you, with almost no code",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/myfatemi04/webparsa",
    packages=[
        "webparsa"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
    python_requires=">=3.6"
)