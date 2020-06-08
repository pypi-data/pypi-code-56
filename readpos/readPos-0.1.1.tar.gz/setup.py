import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
     name='readPos',  
     version='0.1.1',
     author="David Morales",
     author_email="dmorales@odec.es",
     description="Read plain text file data from csv map",
     long_description=long_description,
	 packages=['readPos'],
	 install_requires=['pandas>=0.25.3'],
     long_description_content_type="text/markdown",
     url="http://github.com/dmoralesl",
     classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
     ],
 )