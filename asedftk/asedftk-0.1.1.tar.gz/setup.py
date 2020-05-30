from setuptools import setup

__version__ = "0.1.1"


def readme():
    with open('README.md') as f:
        return f.read()


setup(
    name='asedftk',
    description='DFTK-based calculator for ASE',
    long_description=readme(),
    long_description_content_type="text/markdown",
    keywords=[
        "density-functional", "theory", "DFT", "computational", "chemistry",
        "quantum", "materials", "science", "electronic", "structure", "ab-initio",
        "pseudopotential", "analysis", "ASE", "DFTK"
    ],
    #
    author="Michael F. Herbst",
    author_email="info@michael-herbst.com",
    license="MIT",
    url="https://github.com/mfherbst/ase-dftk",
    #
    version=__version__,
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Topic :: Scientific/Engineering :: Mathematics",
        "Topic :: Scientific/Engineering :: Physics",
        "Topic :: Scientific/Engineering :: Chemistry",
    ],
    #
    packages=["asedftk"],
    package_data={"asedftk": ["calculator.jl"]},
    zip_safe=False,
    python_requires=">=3.6",
    install_requires=[
        "ase>=3",
        "julia>=0.5",
        "numpy>=1.14",
        "pymatgen>=2019.9.16"
    ],
)
