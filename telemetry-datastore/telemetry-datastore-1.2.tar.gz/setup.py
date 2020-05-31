
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="telemetry-datastore",
    version="1.2",
    author="Carlos Tangerino",
    author_email="carlos.tangerino@gmail.com",
    description="Telemetry data store",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Tangerino/telemetry-datastore.git",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)
