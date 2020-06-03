import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="einput",
    version="0.1",
    author="Lucifer Monao",
    author_email="lucifermonao@gmx.com",
    description="A input manager",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/LuciferMonao",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
