import json
import setuptools

kwargs = json.loads("""
{
    "name": "cdk-serverless-api",
    "version": "0.0.3",
    "description": "A sample JSII construct lib for AWS CDK",
    "license": "Apache-2.0",
    "url": "https://github.com/pahud/awscdk-jsii-template.git",
    "long_description_content_type": "text/markdown",
    "author": "Pahud Hsieh<hunhsieh@amazon.com>",
    "project_urls": {
        "Source": "https://github.com/pahud/awscdk-jsii-template.git"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "cdk_serverless_api",
        "cdk_serverless_api._jsii"
    ],
    "package_data": {
        "cdk_serverless_api._jsii": [
            "cdk-serverless-api@0.0.3.jsii.tgz"
        ],
        "cdk_serverless_api": [
            "py.typed"
        ]
    },
    "python_requires": ">=3.6",
    "install_requires": [
        "jsii>=1.6.0, <2.0.0",
        "publication>=0.0.3",
        "aws-cdk.aws-apigatewayv2>=1.44.0, <2.0.0",
        "aws-cdk.aws-lambda>=1.44.0, <2.0.0",
        "aws-cdk.core>=1.44.0, <2.0.0",
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
