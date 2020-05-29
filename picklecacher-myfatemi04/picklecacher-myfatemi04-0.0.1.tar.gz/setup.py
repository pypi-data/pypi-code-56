import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()
    
setuptools.setup(
    name="picklecacher-myfatemi04",
    version="0.0.1",
    author="Michael Fatemi",
    author_email="myfatemi04@gmail.com",
    description="A package that lets you cache your function outputs between runs",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/myfatemi04/picklecache",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
    python_requires=">=3.6"
)