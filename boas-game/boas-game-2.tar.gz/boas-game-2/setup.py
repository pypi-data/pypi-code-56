import setuptools

with open("README.txt", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="boas-game",
    version="2",
    author="abakh",
    author_email="abakh@tuta.io",
    scripts=["boas"],
    description="Collect coins along with rats while being chased by snakes",
    long_description=long_description,
    long_description_content_type="text/plain",
    url="https://github.com/abakh/boa",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=2.7',
)

