#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

def get_detail(ItemName:str):
    with open("gitlab_management/__init__.py") as f:
        for line in f:
            if line.startswith("__" + ItemName + "__"):
                return eval(line.split("=")[-1])

def get_base_detail(ItemName:str):
    with open("gitlab_management/base.py") as f:
        for line in f:
            if line.startswith("__" + ItemName + "__"):
                return eval(line.split("=")[-1])


setuptools.setup(
    name=get_base_detail('title'), 
    version=get_base_detail('version'),
    author=get_detail('author'),
    author_email=get_detail('email'),
    description="GitLab group configuration as code",
    license=get_detail('licence'),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/nofusscomputing/projects/python-gitlab-management",
    project_urls = {
        "Bug Tracker": "https://gitlab.com/nofusscomputing/projects/python-gitlab-management/-/issues",
        "Documentation": "https://python-gitlab-management.readthedocs.io/",
        "Source Code": "https://gitlab.com/nofusscomputing/projects/python-gitlab-management"
    },
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)