import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="voidscript-python-wrapper",
    version="0.0.2",
    author="rmountjoy",
    author_email="ross.mountjoy@gmail.com",
    description="Wrapper for the VoidScript API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/rmountjoy92/VoidScriptPythonWrapper",
    install_requires = ["requests>=2", "six>=1.10"],
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)