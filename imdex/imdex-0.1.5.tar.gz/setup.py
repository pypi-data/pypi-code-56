import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="imdex",
    version="0.1.5",
    author="Lucas Frota",
    author_email="lucv.frota@gmail.com",
    description="Imdex is a library that allows semantic searches over images sets",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Lucasfrota/imdex",
    install_requires=[
        'pandas',
        'numpy',
        'pickle-mixin',
        'tensorflow',
        'pyemd',
        'googledrivedownloader'
    ],
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ]
)
