"""Fichier set up"""
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='affapy',
    version='0.1',
    author="Quentin DESCHAMPS",
    author_email="quentin.deschamps@etu.sorbonne-universite.fr",
    description="A Python library for multiprecision Affine Arithmetic",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.lip6.fr/hilaire/affapy",
    packages=["affapy"],
    install_requires=["mpmath"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.5',
)
