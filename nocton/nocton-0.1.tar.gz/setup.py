from setuptools import setup, find_packages

with open("README.md", "r", encoding='utf-8') as fh:
    long_description = fh.read()

setup(
    name="nocton",
    version="0.1",
    author="Paulo Eduardo de Lima Lourenço",
    author_email="pauloeduardodelima155@gmail.com",
    description="Um app simples para API's que utiliza django-rest-framework",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/PauloE314/nocton",
    packages=find_packages(),
    classifiers=[
        "Environment :: Web Environment",
        "Framework :: Django",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Topic :: Internet :: WWW/HTTP"
    ],
    install_requires = [
        'django',
        'djangorestframework',
        'psycopg2',
        'django-cors-headers'
    ],
    python_requires='>=3.0'
)