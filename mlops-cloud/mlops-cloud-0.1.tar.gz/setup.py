import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="mlops-cloud",
    version="0.1",
    author="Petter Gustafsson",
    download_url="https://github.com/mlops-cloud/sdk/archive/0.1.tar.gz",
    author_email="petter@mlops.cloud",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://mlops.cloud",
    packages=setuptools.find_packages(),
    install_requires=[
        "gql==2.0.0",
        "pandas==1.0.4",
        "joblib==0.15.1",
        "fastparquet==0.4.0",
    ],
)
