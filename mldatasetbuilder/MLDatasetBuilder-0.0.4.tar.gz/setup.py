import setuptools

with open("README.md", "r") as fh:
  long_description = fh.read()

setuptools.setup(
  name="MLDatasetBuilder",
  version="0.0.4",
  author="Karthick Nagarajan",
  author_email="karthick965938@gmail.com",
  description="Python package for build dataset for Machine Learning",
  long_description=long_description,
  long_description_content_type="text/markdown",
  keywords='imagedataset preparedataset prepareimage dataset mldataset datasetbuilder mldatasetbuilder',
  license='MIT',
  url="https://github.com/karthick965938/ML-Dataset-Builder",
  packages=setuptools.find_packages(),
  install_requires=[
    'matplotlib',
    'opencv-python',
    'pandas',
    'torch',
    'torchvision',
  ],
  classifiers=[
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
  ],
  python_requires='>=3.6',
)