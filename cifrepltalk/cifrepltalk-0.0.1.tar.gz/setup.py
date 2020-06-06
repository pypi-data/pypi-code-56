import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="cifrepltalk",
    version="0.0.1",
    author="RaidTheWeb",
    author_email="therealraidtheweb@gmail.com",
    description="A Repl.it Talk Bot Framework for Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/CIFProject/cifrepltalk",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
