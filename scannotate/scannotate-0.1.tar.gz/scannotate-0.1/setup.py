from setuptools import setup, find_packages

package_name = "scannotate"

author = "Tommy Boucher, Noah Spies, Mukund Varma"
author_email = "tboucher@celsiustx.com, npsies@celsiustx.com, mvarma@celsiustx.com"

setup(
    author=author,
    author_email=author_email,
    classifiers=[
        "Development Status :: 1 - Planning",
        "Programming Language :: Python :: 3.7",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: POSIX :: Linux",
    ],
    name=package_name,
    description="Semi-supervised cell-type annotation in single cell RNASeq data",
    url="http://github.com/celsiustx/scannotate/",
    include_package_data=True,
    packages=[],
    version=0.1,
)
