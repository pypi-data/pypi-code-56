import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="tegstats",
    version="0.0.5",
    author="Thomas E Gladwin",
    author_email="thomasgladwin@hotmail.com",
    description="Multiple and hierarchical regression and repeated measures ANOVA",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/thomasgladwin/teg_RMA",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
