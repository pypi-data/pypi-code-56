from setuptools import find_packages, setup


with open("README.md") as f:
    readme = f.read()

install_requires = [
    "apache-airflow<2.0.0",
    "neuromation>=20.4.6",
    "typing_extensions>=3.7.4",
]

setup(
    name="neuro-airflow-plugin",
    version="0.0.1",
    url="https://github.com/neuromation/platform-airflow-plugin",
    packages=find_packages(include=("neuro_airflow_plugin", "neuro_airflow_plugin.*")),
    install_requires=install_requires,
    python_requires=">=3.7",
    entry_points={
        "airflow.plugins": "neuro_plugin=neuro_airflow_plugin.neuro_plugin:NeuroPlugin"
    },
    include_package_data=True,
    description="Neu.ro Airflow plugin",
    long_description=readme,
    long_description_content_type="text/markdown; charset=UTF-8; variant=GFM",
    author="Neu.ro Team",
    author_email="team@neu.ro",
    license="Apache License, version 2.0",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: Other/Proprietary License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Environment :: Plugins",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Information Technology",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Software Development",
        "Topic :: Utilities",
        "License :: OSI Approved :: Apache Software License",
    ],
)
