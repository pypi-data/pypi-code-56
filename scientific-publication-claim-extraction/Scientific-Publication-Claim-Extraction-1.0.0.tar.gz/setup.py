import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Scientific-Publication-Claim-Extraction", # Replace with your own username
    version="1.0.0",
    author="Xi Chen",
    author_email="bchen@juvenatherapeutics.com",
    description="This package could be used to extract claims from scientific publication",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/juvena-therapeutics/scientific-claim",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)