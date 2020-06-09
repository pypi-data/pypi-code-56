""" setup.py created according to https://packaging.python.org/tutorials/packaging-projects """

import setuptools #type:ignore

setuptools.setup(
    name="quetz",
    version="0.0.0",
    author="hashberg",
    author_email="sg495@users.noreply.github.com",
    description="A Python library for compositional programming.",
    url="https://github.com/hashberg-io/quetz",
    packages=setuptools.find_packages(exclude=["test"]),
    classifiers=[ # see https://pypi.org/classifiers/
        "Programming Language :: Python :: 3.7",
        "Operating System :: OS Independent",
        "Development Status :: 1 - Planning",
        "Natural Language :: English",
        "Typing :: Typed",
    ],
    package_data={"": [],
                  "quetz": ["quetz/py.typed"],
                 },
    include_package_data=True
)
