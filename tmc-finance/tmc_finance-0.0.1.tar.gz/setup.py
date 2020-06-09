import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="tmc_finance",
    version="0.0.1",
    author="Yifei Yu",
    author_email="yyu.mam2020@london.edu",
    description="A package developed to create a summary of London Business School's Tech & Media Club's financial position",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/MacarielAerial/tmc_finance",
    download_url="https://github.com/MacarielAerial/tmc_finance/archive/v_0.0.1.tar.gz",
    keywords=['SUMMARY','FINANCE','LONDONBUSINESSSCHOOL'],
    install_requires=['numpy','pandas','matplotlib'],
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
