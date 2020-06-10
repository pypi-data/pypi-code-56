import setuptools

with open("README.md", "r") as f:
    long_desc = f.read()

setuptools.setup(
    name="alphamini",
    version="0.0.10",
    author='logic.peng',
    autho_email='logic.peng@ubtrobot.com',
    description="python sdk for ubtenic alphamini robot",
    long_description=long_desc,
    long_description_content_type="text/markdown",
    # url="",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'websockets',
        'ifaddr',
        'protobuf'
    ],
)
