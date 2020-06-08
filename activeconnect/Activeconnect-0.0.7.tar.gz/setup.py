import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Activeconnect",
    version="0.0.7",
    author="Activeconnect",
    author_email="support@activeconnect.io",
    description="Python package to access Activeconnect API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    install_requires=[
          'marshmallow-dataclass',
          'marshmallow-enum'
      ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)