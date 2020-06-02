import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="quple", 
    version="0.0.1",
    author="Alkaid Cheng",
    author_email="chi.lung.cheng@cern.ch",
    description="A framework for quantum machine learning using the google Cirq library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.cern.ch/clcheng/quple",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[   
          'numpy'],
    python_requires='>=3.6',
)
