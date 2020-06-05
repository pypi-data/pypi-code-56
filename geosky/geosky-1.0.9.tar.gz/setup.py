from setuptools import setup

def readme():
    with open('README.md') as f:
        README = f.read()
    return README



setup(
    name="geosky",
    version="1.0.9",
    description="A Python package to get all city country and stat names",
    long_description=readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/jyotiprakash-work/geosky",
    author="jyotiprakash panigrahi",
    author_email="jyotiprakash.work@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
    ],
    packages=["geosky"],
    include_package_data=True,
    install_requires=["requests"],
    package_data={'geosky':['cities.json']}
    
)