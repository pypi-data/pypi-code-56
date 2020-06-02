import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="urlock", # Replace with your own username
    version="0.1.8",
    author='David Kerschner',
    author_email='dkerschner@gmail.com',
    description="Library for talking to a running Urbit ship over http",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/baudtack/urlock',
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)