import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="nltkPackagedevops", # Replace with your own username
    version="0.0.31",
    author="Ravi Teja Kondisetty",
    author_email="kondisettyravi@gmail.com",
    description="A small example package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kondisettyravi/nltkTransformer",
    packages=['nltkTransformer', 'nlp'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
    package_data={
      "nltkTransformer": ["*"],
      "nlp": ["*"]
    },
    include_package_data=True
)