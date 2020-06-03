import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="LASExplanation",
    version="0.0.1",
    author="Kewen Peng",
    author_email="kpeng@ncsu.edu",
    description="This package is a brief wrap-up toolkit built based on 2 explanation packages: LIME and SHAP. The package contains 2 explainers: LIMEBAG and SHAP. It takes data and fitted models as input and returns explanations about feature importance ranks and/or weights. (etc. what attributes matter most within the prediction model).", 
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kpeng2019/LAS",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3',
    install_requires=[
        'pandas',
        'numpy',
        'lime',
        'shap',
        'scikit-learn',
        'setuptools',
        'ipython',
    ],
    package_data={
        'LASExplanation': ['camel-1.2.csv'],
    },
    include_package_data=True,
)
