import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ethutil", # Replace with your own username
    version="0.0.5",
    author="CS",
    author_email="362228416@qq.com",
    description="eth utils",
    long_description=long_description,
    long_description_content_type="text/markdown",
    py_modules=["ethutil"],
    url="https://github.com/362228416/ethutils-py",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)