from setuptools import setup


def readme():
    with open('README.md') as f:
        read_me = f.read()
    return read_me


setup(
    name="draw-missing",
    version="1.0.0",
    description="A Python package to visualize missing values in a data frame",
    long_description=readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/Tejas003/draw_missing",
    author="Tejas Sanjay Shinde",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Operating System :: OS Independent",
    ],
    py_modules=["drawmissing"],
    install_requires=["matplotlib"],
    package_dir={'': 'Draw-Missing'}

)



