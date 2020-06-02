import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="only-utils",
    version="0.0.1",
    author="Jose Salas",
    description="Only utils",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/developerjoseph/only-utils",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[]
)
