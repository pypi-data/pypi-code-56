import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="inforion", # Replace with your own username
    version="0.0.4",
    author="Dnaiel Jordan",
    author_email="daniel.jordan@feellow-consulting.de",
    description="Infor ION Package for Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dajor/inforion",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
