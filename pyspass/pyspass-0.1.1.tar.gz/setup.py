import setuptools

with open("README.rst", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyspass",
    version="0.1.1",
    author="Stefan Seltmann",
    author_email="s.seltmann06@web.de",
    description="pyspass",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    url='https://github.com/stefanseltmann77/pyspass',
    packages=['pyspass'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)
