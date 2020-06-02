import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="graph_writer", # Replace with your own username
    version="0.1.1",
    author="Partha Ghosh, Pravir Singh Gupta",
    author_email="parthaghosh.iitbbs@gmail.com, pravir.singh.gupta@gmail.com",
    description="This repository is intended to visualize and publish interactive computation graphs such as PyTorch Networks, Tensorflow Networks etc.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/GuptaPravirSingh/graph_writer",
    packages=setuptools.find_packages(),
    py_modules=['graph_writer'],
    install_requires=['networkx', 'matplotlib', 'wrapt', 'pyvis'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)