################################################################################
#https://packaging.python.org/tutorials/packaging-projects/
#python setup.py sdist bdist_wheel
#python -m twine upload --repository-url https://test.pypi.org/legacy/ dist/*
#pip install --index-url https://test.pypi.org/simple/ --no-deps aws-access-rajdeb
#C:\aws-saml-access\token - this is where I have my PYPI token
###python -m twine upload dist/*
#python -m aws_access_util.get_aws_access
###############################################################################
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="aws-access", # Replace with your own username
    version="1.0.8",
    author="Rajib Deb",
    author_email="rajdeb@cisco.com",
    description="This package is used to get temporary token for aws access",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://bitbucket-eng-sjc1.cisco.com/bitbucket/scm/con/hyperloop.git",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
    install_requires=[
          'requests',
          'beautifulsoup4==4.8.2',
          'jinja2',
          'configparser',
          'boto',
           'boto3',
           'botocore',
           'awscli',
           'defusedxml'
      ]
)