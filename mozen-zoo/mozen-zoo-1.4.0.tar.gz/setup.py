import setuptools

setuptools.setup(
    name="mozen-zoo", 
    version="1.4.0",
    author="SAMBOU Augustin",
    author_email="aniamba-amaye.sambou@etu.univ-amu.fr",
    description="Python library of Mozen web site",
    long_description="",
    url="https://gitlab.lis-lab.fr/augustin.sambou/mozen.git",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)