from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name             = 'h3ppy',
    version          = '0.1',
    author           = 'Henrik Melin',
    author_email     = 'h.melin@gmail.com',
    description      = 'Model and fit H3+ spectra',
    url              = 'https://github.com/henrikmelin/h3ppy',
    keywords         = 'infrared spectroscopy H3+ modelling',
    packages         = find_packages(),
    install_requires = ['numpy'], 
    package_data={ 'h3p_line_data': ['h3p_line_list_neale_1996_subset.txt'],},

    long_description=long_description,
    long_description_content_type="text/markdown",
#    packages=[envstring("NAME"), envstring("NAME") + ".main"],
    classifiers=[
        "Operating System :: POSIX :: Linux",
        "License :: OSI Approved :: MIT License",
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
)
