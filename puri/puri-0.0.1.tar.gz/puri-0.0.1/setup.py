import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='puri', # Replace with your own username
    version="0.0.1",
    author='Puri Phakmongkol',
    author_email='puri.pmk@gmail.com',
    description='A personal tools for make everythings easy !',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/suakow/puri",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)