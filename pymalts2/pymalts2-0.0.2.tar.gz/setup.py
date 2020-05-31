import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pymalts2",
    version="0.0.2",
    author="Harsh Parikh",
    author_email="harsh.parikh@duke.edu",
    description="Causal Inference Matching Package.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/almost-matching-exactly/MALTS",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)