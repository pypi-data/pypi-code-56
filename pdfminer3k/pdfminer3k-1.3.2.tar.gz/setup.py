import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pdfminer3k", # Replace with your own username
    version="1.3.2",
    author="Example Author",
    author_email="author@example.com",
    description="Forked from original pdfminer",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/canserhat77/pdfminer3k",
    download_url="https://github.com/canserhat77/pdfminer3k/archive/v1.3.1.tar.gz",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)