
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

with open("version", "r") as f:
    version = f.read()

setuptools.setup(
    name="awesome-research-demo-package",
    version=version,
    author="",
    author_email="",
    description="",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    packages=setuptools.find_packages(),
    keywords=[],
    classifiers=[
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    install_requires=[
        'numpy==1.17.3'
    ],
    python_requires='>=3.6',
)
