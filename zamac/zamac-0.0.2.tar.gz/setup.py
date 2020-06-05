import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="zamac",
    version="0.0.2",
    author="Zama Team",
    author_email="hello@zama.ai",
    description="Zama compiler",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://zama.ai",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
