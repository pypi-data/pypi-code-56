#from distutils.core import setup
import setuptools

with open("README", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name = 'cloudeos',
    packages = ['.'],
    version = '0.1.1',
    description = 'https://cloudeos.com api sdk',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author = 'Cloudeos',
    author_email = 'team@cloudeos.com',
    url = 'https://github.com/hknyldz/CloudeosApi',
    keywords = ['cloud', 'cloudeos'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.5',
)
