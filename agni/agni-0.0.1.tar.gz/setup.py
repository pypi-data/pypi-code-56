import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="agni",
    version="0.0.1",
    author="Deven Parekh",
    author_email="deven.parekh@mail.mcgill.ca",
    description=(
        "AGNI (AutoGrader with Nice Interface),"
        " a Python assignment grading tool and a companion to Codepost. (Work in progress)"),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/d3vp/agni",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
