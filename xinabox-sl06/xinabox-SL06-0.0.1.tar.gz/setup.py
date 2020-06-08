import setuptools
with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="xinabox-SL06",
    version="0.0.1",
    author="Luqmaan Baboo",
    author_email="luqmaanbaboo@gmail.com",
    description="Proximity, gesture, light and colour sensor",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/xinabox/Python-SL06",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
