import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="biocwl-dash", # Replace with your own username
    version="0.0.6",
    author="Jacob Roberts",
    author_email="jacoberts@gmail.com",
    description="Viewer for Mount Sinai IIDSGT Precision Oncology reports.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/iidsgt/biocwl-dash",
    packages=['biocwl_dash', 'biocwl_dash.pages'],
    package_data={'biocwl_dash': ['assets/*']},
    install_requires=[
        'dash',
        'flask',
        'dash-rabix',
        'dash-lazylog',
        'pandas',
        'pdf2image',
        'dash-table',
        'pyyaml',
        'dash-bio'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)


print(setuptools.find_namespace_packages(include=['biocwl_dash','biocwl_dash.*']))