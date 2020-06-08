import pathlib
from setuptools import setup

# the directory containing this file
HERE = pathlib.Path(__file__).parent

def readme():
    with open('README.md') as f:
        README = f.read()
    return README


setup(
    name="raghu3",
    version="3.0.0",
    description="A Python package to test in local",
	py_modules=['raghu'],
	
    long_description=readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/Raghu960/raghu",
    author="Raghavendra Deshmukh",
    author_email="raghu.deshmukh55@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["raghu"],
    include_package_data=True,
    entry_points={
        "console_scripts": [
            "raghu=raghu.main:main",
            ]
        },
)
