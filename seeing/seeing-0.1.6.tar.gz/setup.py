import setuptools

from seeing import __version__

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="seeing", # Replace with your own username
    version=__version__,
    author="Mikele",
    author_email="blive200@gmail.com",
    description="Monitor & auto execute single script(go py c) after modify.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/toyourheart163/seeing",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={
        'console_scripts': ['seeing = seeing:main']
    },
    python_requires='>=3.6',
)
