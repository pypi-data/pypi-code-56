import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pnp_datetime", # Replace with your own username
    version="0.7.0",
    author="PyPnP",
    author_email="pypnp@protonmail.com",
    description='Python Plug and Play style datetime',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/pypnp/pnp_datetime',
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
