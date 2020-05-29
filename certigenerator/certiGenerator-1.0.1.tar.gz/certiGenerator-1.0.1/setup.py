import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="certiGenerator", # Replace with your own username
    version="1.0.1",
    author="yathartharora",
    author_email="yathartharora1999@gmail.com",
    description="Easily generate participation certificates using this package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yathartharora/event_certificates",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.0',
)
