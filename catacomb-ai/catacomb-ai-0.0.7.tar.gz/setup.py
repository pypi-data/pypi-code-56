import pathlib
from setuptools import setup

HERE = pathlib.Path(__file__).parent

setup(
    name='catacomb-ai',
    version='0.0.7',
    description="Build tools for Catacomb's model hosting suite.",
    packages=['catacomb'],
    install_requires=['click'],
    include_package_data=True
)