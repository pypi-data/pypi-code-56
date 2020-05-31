from setuptools import setup, find_packages

setup(
    name='dt4j',
    description="This is a Package to handle java source code",
    packages=find_packages(),
    version='0.1.0',
    install_requires=[
        'javalang',
        'nltk'
    ]
)
