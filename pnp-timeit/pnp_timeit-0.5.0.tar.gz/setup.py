import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pnp_timeit",
    version="0.5.0",
    author="PyPnP",
    author_email="pypnp@protonmail.com",
    description='Measure execution time of small code snippets, write to log',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/pypnp/pnp_timeit',
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
