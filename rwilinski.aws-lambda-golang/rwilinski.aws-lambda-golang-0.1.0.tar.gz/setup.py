import json
import setuptools

kwargs = json.loads("""
{
    "name": "rwilinski.aws-lambda-golang",
    "version": "0.1.0",
    "description": "CDK Construct for AWS Lambda in Golang",
    "license": "Apache-2.0",
    "url": "https://github.com/RafalWilinski/aws-lambda-golang-cdk",
    "long_description_content_type": "text/markdown",
    "author": "Rafal Wilinski<raf.wilinski@gmail.com>",
    "project_urls": {
        "Source": "https://github.com/RafalWilinski/aws-lambda-golang-cdk.git"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "rwilinski.aws-lambda-golang",
        "rwilinski.aws-lambda-golang._jsii"
    ],
    "package_data": {
        "rwilinski.aws-lambda-golang._jsii": [
            "aws-lambda-golang@0.1.0.jsii.tgz"
        ],
        "rwilinski.aws-lambda-golang": [
            "py.typed"
        ]
    },
    "python_requires": ">=3.6",
    "install_requires": [
        "jsii>=1.6.0, <2.0.0",
        "publication>=0.0.3",
        "aws-cdk.aws-lambda>=1.43.0, <2.0.0",
        "aws-cdk.core>=1.43.0, <2.0.0",
        "constructs>=3.0.3, <4.0.0"
    ],
    "classifiers": [
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: JavaScript",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Typing :: Typed",
        "Development Status :: 4 - Beta",
        "License :: OSI Approved"
    ]
}
""")

with open('README.md') as fp:
    kwargs['long_description'] = fp.read()


setuptools.setup(**kwargs)
