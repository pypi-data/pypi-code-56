import setuptools
with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="mcvoronoi",
    version="0.0.3",
    author="Kusum Kumari",
    author_email="kusum.kumarisjce@gmail.com",
    description="mcvoronoi package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/abcnishant007/mcvoronoi",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
