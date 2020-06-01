import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="leetnode",
    version="1.0.0",
    author="Jeffrey Thomas Piercy",
    author_email="mqduck@mqduck.net",
    description="A small Python 3.6+ library to make debugging LeetCode binary tree, linked list and matrix problems "
                "more convenient.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/MQDuck/LeetNode",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)