import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="tab_gan_metrics",
    version="v1.1.4",
    author="Tavva Prudhvith",
    author_email="iamsinglemap@gmail.com",
    description="A package to evaluate how close a synthetic data set is to real data.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ChillBoss/tab_gan_metrics",
    packages=setuptools.find_packages(),
    install_requires=[
        'pandas',
        'numpy',
        'tqdm',
        'psutil',
        'dython==0.5.1',
        'seaborn',
        'matplotlib',
        'scikit-learn',
        'scipy'
    ],
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "Operating System :: OS Independent",
    ],
)
