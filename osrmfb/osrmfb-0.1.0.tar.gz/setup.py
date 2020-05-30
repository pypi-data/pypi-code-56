import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="osrmfb",  # Replace with your own username
    version="0.1.0",
    author="chang@nextbillion.ai",
    author_email="chang@nextbillion.ai",
    description="osrm flatbuffer def",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
    ],
    python_requires='>=3.6',
    include_package_data=True,
)
