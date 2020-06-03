from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


setup(
    name="bnbxrate",
    version="0.1.0",
    author="Hristo Mavrodiev",
    author_email="h.mavrodiev@abv.bg",
    description="Bulgarian National Bank - get history exchage rates",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/hristo-mavrodiev/bnbxrate",
    include_package_data=True,
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'bnbxrate=bnbxrate.bnb:main'
        ]
    }
)
