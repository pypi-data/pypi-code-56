

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
     name='Medeina',  
     version='1.01',
     author="Daniel Davies",
     author_email="dd16785@bristol.ac.uk",
     description="A cumulative food web",
     long_description="hello",
     long_description_content_type=long_description,
     url="https://github.com/Daniel-Davies/Medeina",
     packages=setuptools.find_packages(),
     classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
     ],
     install_requires=['pycountry','pandas','taxon_parser'],
 )