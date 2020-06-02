import re

import setuptools


def read_file(path):
    with open(path, "r") as handle:
        return handle.read()


def read_version():
    try:
        s = read_file("VERSION")
        m = re.match(r"v(\d+\.\d+\.\d+(-.*)?)", s)
        return m.group(1)
    except FileNotFoundError:
        return "0.0.0"


long_description = read_file("docs/source/description.rst")
version = read_version()

setuptools.setup(
    name="shu",
    description="""
    REST API on top of Airflow
    """,
    keywords="airflow,api,rest",
    long_description=long_description,
    include_package_data=True,
    version=version,
    url="https://gitlab.com/greenhousegroup/ai/libraries/shu/",
    author="Greenhouse AI team",
    author_email="ai@greenhousegroup.com",
    package_dir={"shu": "src/shu"},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
    ],
    install_requires=[
        "flask-restplus == 0.13.*",
        "spectacular>=0.2.0,<=0.3.0",
        "apache-airflow",
    ],
    entry_points={"airflow.plugins": ["shu = shu.plugin:Plugin"]},
    data_files=[(".", ["VERSION"])],
    setup_requires=["pytest-runner"],
    tests_require=["pytest>=4"],
    packages=setuptools.find_packages("src"),
)
