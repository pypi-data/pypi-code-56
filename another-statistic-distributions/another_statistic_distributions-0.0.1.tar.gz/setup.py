import setuptools

DISTNAME = 'another_statistic_distributions'
DESCRIPTION = 'Python modules for Gaussian and Binomial distributions'
with open('README.md') as f:
    LONG_DESCRIPTION = f.read()
AUTHOR = 'Muthahhari A. Padmanagara'
AUTHOR_EMAIL = 'muthahharipadmanagara@gmail.com'
URL = 'https://github.com/crowsad/another-statistic-distributions'
LICENSE = 'MIT License'
PACKAGES = ['another_statistic_distributions']


setuptools.setup(
    name=DISTNAME,
    version="0.0.1",
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    description=DESCRIPTION,
    license=LICENSE,
    long_description=LONG_DESCRIPTION,
    url=URL,
    packages=PACKAGES,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
