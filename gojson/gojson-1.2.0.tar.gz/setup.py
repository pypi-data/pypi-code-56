import setuptools
import os

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setuptools.setup(name="gojson",
    version="1.2.0",
    description="A python library for https://db.neelr.dev/",
    long_description=read("README.md"),
    url="https://github.com/AgeOfMarcus/gojson",
    author="AgeOfMarcus",
    author_email="marcus@marcusweinberger.com",
    packages=setuptools.find_packages(),
    zip_safe=False,
    install_requires=['requests', 'jsonpickle']
)
