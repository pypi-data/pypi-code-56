import setuptools

with open("README.md", "r") as f:
    long_desc = f.read()

setuptools.setup(
    name="alphamini",
    version="0.0.8",
    author='logic.peng',
    autho_email='logic.peng@ubtrobot.com',
    description="python sdk for ubtenic alphamini robot",
    long_description = long_desc,
    long_description_content_type="text/markdown",
    # url="",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'websockets >= 8.1',
        'ifaddr >=0.1.6',
        'protobuf >= 3.12.2'
    ],
)
