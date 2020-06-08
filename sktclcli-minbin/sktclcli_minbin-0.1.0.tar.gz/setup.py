import setuptools

with open("readme.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="sktclcli_minbin",  # add your username to ensure uniqueness
    version="0.1.0",
    author="daominah",
    author_email="tung.dao@techx.vn",
    description="A client in Python to connect to socket cluster server",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/daominah/sktclcli_minbin",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
