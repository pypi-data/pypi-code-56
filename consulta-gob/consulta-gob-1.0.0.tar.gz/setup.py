import setuptools

def readme():
    with open("README.md", "r") as f:
        README = f.read()
        return README


setuptools.setup(
    name="consulta-gob", # Replace with your own username
    version="1.0.0",
    author="Partum",
    author_email="partum.sts@gmail.com",
    description="Packete para conultar info relacionada con CURP",
    long_description=readme(),
    long_description_content_type="text/markdown",
    url="",
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=["curp"],
    include_package_data=True,
    install_requires=["requests"]
)
