import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="cryptraider", # Replace with your own username
    version="0.0.1",
    author="Dane",
    author_email="dslh.4cad@gmail.com",
    description="A collection of cryptanalysis utilities for CTF challenges",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/4cad/CryptRaider",
    packages=['cryptraider', 'cryptraider/math', 'cryptraider/cipher', 'cryptraider/derand'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: POSIX :: Linux",
    ],
    package_dir = {'': 'src'},
    install_requires=[
        'gmpy2'
    ],
    python_requires='>=3.6',
)