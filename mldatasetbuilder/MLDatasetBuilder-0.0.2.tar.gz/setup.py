import setuptools

with open("README.md", "r") as fh:
  long_description = fh.read()

setuptools.setup(
  name="MLDatasetBuilder",
  version="0.0.2",
  author='Karthick Nagarajan',
	author_email='karthick965938@gmail.com',
  description="Build a Package for Machine Learning Dataset",
  long_description=long_description,
  long_description_content_type="text/markdown",
  license='MIT',
  url="https://github.com/karthick965938/ML-Dataset-Builder",
  packages=['MLDatasetBuilder'],
  classifiers=[
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
  ],
  python_requires='>=3.6',
)