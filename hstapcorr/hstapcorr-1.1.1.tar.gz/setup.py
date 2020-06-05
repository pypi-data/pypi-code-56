import setuptools

setuptools.setup(
    name="hstapcorr",
    version="1.1.1",
    author="Kornpob Bhirombhakdi",
    author_email="kbhirombhakdi@stsci.edu",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/bkornpob/hstapcorr",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 2"
        ,"License :: OSI Approved :: MIT License"
        ,"Operating System :: OS Independent"
    ],
    python_requires='>=2.'
)
