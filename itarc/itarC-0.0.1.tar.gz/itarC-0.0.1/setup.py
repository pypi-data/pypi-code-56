from setuptools import setup, find_packages

def readme():
    with open('README.md') as f:
        README = f.read()
    return README
        

setup(
    name ="itarC",
    version = "0.0.1",
    description="A python package to register or view fake job alerts",
    long_description=readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/startng/forward4-itarj-adekams",
    author="Adenike Salau",
    author_email="kifademi@gmail.com",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.7",
    ],
    keywords = "fake job alerts",
    packages=find_packages(),
    package_data = {'itarj_console': ['*.txt']},
    include_package_data = True,
    install_requires = ["requests"],
    entry_points = {
        "console_scripts": [
            "itarj-console=itarj_console.itarj:main",
        ],
    }   
)

