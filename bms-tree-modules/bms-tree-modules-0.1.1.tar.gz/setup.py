from setuptools import find_packages, setup

setup(
    name="bms-tree-modules",
    version="0.1.1",
    packages=find_packages(exclude=["tests", "files", "src/utils"]),
    package_data={"": ["LICENSE", "NOTICES"]},
    python_requires=">=3.8",
    setup_requires=[],
    install_requires=["typing"],
    extras_require={
        "dev": ["pylama", "black", "flake8"],
        "tests": ["pytest", "pytest-watch"],
    },
    include_package_data=True,
    author="Moritz Eck",
    author_email="moritz.eck@gmail.com",
    description="The package has been created as part of the BMS20 project at the Institue of Banking & Finance and Institute of Informatics (University of Zurich). It allows to create a tree data structure recursively from a given input json/dict. The package delivers the game building blocks for the various components: Node, Tree, Team, Config, Curves, Module.",  # noqa: E501
    url="https://gitlab.uzh.ch/uzh-bf/sim/banking-game-2020",
    project_urls={
        "Documentation": "https://gitlab.uzh.ch/uzh-bf/sim/banking-game-2020",
        "Source Code": "https://gitlab.uzh.ch/uzh-bf/sim/banking-game-2020",
    },
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.8",
    ],
)
