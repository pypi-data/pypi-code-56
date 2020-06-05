import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="howiml",
    version="1.0.0",
    author="Herman Wika Horn",
    author_email="hermanwh@hotmail.com",
    description="A top-level machine learning framework",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/hermanwh/howi-ml",
    packages=['howiml', 'howiml.utils'],
    package_dir={'howiml': 'howiml'},
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6, <3.7',
    install_requires=[
        'Keras>=2.3.1,<2.3.2',
        'matplotlib>=3.2.0,<3.2.1',
        'numpy>=1.18.1,<1.18.2',
        'pandas>=0.25.3,<0.25.4',
        'pandas-profiling>=2.5.0,<2.5.1',
        'prettytable>=0.7.2,<0.7.3',
        'scikit-learn>=0.22.2,<0.22.3',
        'seaborn>=0.10.0,<0.10.1',
        'tensorflow>=2.1.0,<2.1.1',
        'notebook>=6.0.3,<6.0.4',
    ],
)