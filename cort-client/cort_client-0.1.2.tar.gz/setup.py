from setuptools import setup, find_packages
from cort_client import (
    __AUTHOR__,
    __AUTHOR_EMAIL__,
    __LICENSE__,
    __VERSION__,
    __PROJECT_NAME__,
)

setup(
    name=__PROJECT_NAME__,
    version=__VERSION__,
    author=__AUTHOR__,
    author_email=__AUTHOR_EMAIL__,
    packages=find_packages(),
    include_package_data=True,
    license=__LICENSE__,
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    python_requires=">=3.6",
    install_requires=["minadb", "requests", "loguru", "psutil"],
)
