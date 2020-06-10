import json
import setuptools

kwargs = json.loads("""
{
    "name": "cdk-github-import",
    "version": "1.0.0",
    "description": "Import local file assets into a new Github repository",
    "license": "Apache-2.0",
    "url": "https://github.com/pahud/cdk-github-import.git",
    "long_description_content_type": "text/markdown",
    "author": "Pahud Hsieh<hunhsieh@amazon.com>",
    "project_urls": {
        "Source": "https://github.com/pahud/cdk-github-import.git"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "cdk_github_import",
        "cdk_github_import._jsii"
    ],
    "package_data": {
        "cdk_github_import._jsii": [
            "cdk-github-import@1.0.0.jsii.tgz"
        ],
        "cdk_github_import": [
            "py.typed"
        ]
    },
    "python_requires": ">=3.6",
    "install_requires": [
        "jsii>=1.6.0, <2.0.0",
        "publication>=0.0.3",
        "aws-cdk.aws-codestar>=1.45.0, <2.0.0",
        "aws-cdk.aws-s3>=1.45.0, <2.0.0",
        "aws-cdk.aws-s3-assets>=1.45.0, <2.0.0",
        "aws-cdk.core>=1.45.0, <2.0.0",
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
