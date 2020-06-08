import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(name='ucodeio_hellolib',
      version='0.2',
      description='A simple hello library and function that returns hello <name>',
      long_description=long_description,
      long_description_content_type="text/markdown",
      url='http://github.com/sstacha/ucodeio_hellolib',
      author='Steve Stacha',
      author_email='sstacha@gmail.com',
      license='MIT',
      packages=setuptools.find_packages(),
      classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
      ],
      python_requires='>=3.6',
)
