from setuptools import setup, find_packages
from os import path
here = path.abspath(path.dirname(__file__))

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name='Asymptotic Complexity Judge',
    version = '0.0.1',
    packages = find_packages(),
    description = 'Terminal Judge for Asymptotic Complexity',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Ehud Adler",
    author_email="adlerehud@gmail.com",
    python_requires='>=3.5',
    install_requires=[
        'prettytable>=0.7.2',
        'python-dotenv>=0.12',
        'xtermcolor>=1.3',
        'zeroc-ice>=3.7.3',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points = {
        'console_scripts': ['acjudge=ACJudge_Pkg.Client:main'],
    }
)
