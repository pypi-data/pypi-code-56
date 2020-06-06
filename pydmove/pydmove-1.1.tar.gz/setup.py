from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()


setup(
    name="pydmove",
    version="1.1",
    description="mv (using dd followed by rm) with a progressbar",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/avivajpeyi/pydd",
    author="Avi Vajpeyi",
    author_email="avi.vajpeyi@gmail.com",
    license="MIT",
    packages=["pydd"],
    zip_safe=False,
    install_requires=["tqdm>=4.32.1"],
    entry_points={"console_scripts": ["pydd=pydd.pydd:main"]},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
)
