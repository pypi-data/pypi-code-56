import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="mydemode", # Replace with your own username
    version="0.0.3",
    author="Sumit Sharma",
    author_email="sharmasumit64@gmail.com",
    description="Sample test package for DE APIs POC",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/sharmasumit64/mydemode",
    # packages=setuptools.find_packages(where='imp'),
    packages=['mydemode', 'mydemode.imp', 'mydemode.rest', 'mydemode.rest.epf'],
    # package_dir={'': 'src'}
    # scripts=['mydemode/imp/*'],
    # packages=setuptools.find_packages(include=[]),
    classifiers=[
        "Programming Language :: Python :: 3",
        'Programming Language :: Python :: 2.7',
        "Operating System :: OS Independent",
    ],
    python_requires='>=2.7',
)