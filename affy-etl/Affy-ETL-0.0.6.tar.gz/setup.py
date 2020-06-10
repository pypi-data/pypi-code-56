import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Affy-ETL", # Replace with your own username
    version="0.0.6",
    author="Hung Chang",
    author_email="zero102x@gmail.com",
    description="Affydata ETL package",
    long_description="Easy to extract/transform/loading Affy data ",
    long_description_content_type="text/markdown",
    url="https://github.com/dapingtai/Affy-ETL",
    packages=setuptools.find_packages(),
    python_requires='>=3.6',
)