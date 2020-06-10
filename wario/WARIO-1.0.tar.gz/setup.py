import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="WARIO",
    version="1.0",
    author="Oliver Cook, Thomas Mudway, Ron Harwood",
    description="Pipeline backend and node development tools for WARIO",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/McMasterRS/WARIO",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'PyQt5',
        'blinker'
    ],
    python_requires='>=3.6',
)