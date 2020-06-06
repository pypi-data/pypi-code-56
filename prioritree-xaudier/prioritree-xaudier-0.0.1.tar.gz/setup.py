import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="prioritree-xaudier", # Replace with your own username
    version="0.0.1",
    author="Xavier Audier",
    author_email="xetal.contact@gmail.com",
    description="This package contains a graphical interface for project management.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/XavierAudier/prioritree",
    packages=setuptools.find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)