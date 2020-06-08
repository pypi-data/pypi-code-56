#!/usr/bin/env python
# coding: utf-8

# In[1]:


from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="SSG_API_test", # Replace with your own username
    version="0.0.2",
    author="Ho Jun Le",
    author_email="hojunle@outlook.com",
    description="A Python package to get SSG APIs.",
    long_description= long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/hojunle/SSG_API_test",
    packages=["SSG_API_test"],
    include_package_data = True,
    #install_requires=["requests","json","pprint","HTTPBasicAuth"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)


