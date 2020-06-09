"""
# Welcome to `awscdk-jsii-template`

This repository template helps you generate JSII construct library for AWS CDK.

## Confiuguration

1. customize your `.projenrc.js`
2. run `npx projen` to generate the `package.json` and `.github/workflows` from `.projenrc.js`
3. `yarn install` to install all required npm packages

## Integration tests

1. run `yarn watch` in a seperate terminal
2. edit `test/integ.api.ts`
3. `cdk diff` and `cdk deploy`

```bash
cdk --app 'test/integ.api.js' diff
cdk --app 'test/integ.api.js' deploy
```

1. validate the stack

## Unit tests

1. edit `test/*.test.ts`
2. run `yarn test`

## Usage

| Command          | Description                                       |
|------------------|---------------------------------------------------|
|`yarn install`    |Install dependencies                               |
|`yarn compile`    |Compile to JavaScript                              |
|`yarn watch`      |Watch for changes and compile                      |
|`yarn test`       |Run tests                                          |
|`yarn run package`|Create `dist` with bundles for all languages       |
|`yarn build`      |Compile + test + package                           |
|`yarn bump`       |Bump a new version (based on conventional commits) |
|`yarn compat`     |Run API compatibility check against latest         |

## GitHub Workflows

* [Build](./.github/workflows/build.yml): when a PR is created/updated, runs `yarn build`
* [Release](./.github/workflows/release.yml): `yarn build` and publish to all package managers for every commit to `master` (ignore if current version is already released).
"""
import abc
import builtins
import datetime
import enum
import typing

import jsii
import jsii.compat
import publication

from ._jsii import *

import aws_cdk.aws_lambda
import aws_cdk.core


class ServerlessApi(aws_cdk.core.Construct, metaclass=jsii.JSIIMeta, jsii_type="cdk-serverless-api.ServerlessApi"):
    """
    stability
    :stability: experimental
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, handler: typing.Optional[aws_cdk.aws_lambda.IFunction]=None) -> None:
        """
        :param scope: -
        :param id: -
        :param handler: 

        stability
        :stability: experimental
        """
        props = ServerlessApiProps(handler=handler)

        jsii.create(ServerlessApi, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="handler")
    def handler(self) -> aws_cdk.aws_lambda.IFunction:
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "handler")


@jsii.data_type(jsii_type="cdk-serverless-api.ServerlessApiProps", jsii_struct_bases=[], name_mapping={'handler': 'handler'})
class ServerlessApiProps():
    def __init__(self, *, handler: typing.Optional[aws_cdk.aws_lambda.IFunction]=None) -> None:
        """
        :param handler: 

        stability
        :stability: experimental
        """
        self._values = {
        }
        if handler is not None: self._values["handler"] = handler

    @builtins.property
    def handler(self) -> typing.Optional[aws_cdk.aws_lambda.IFunction]:
        """
        stability
        :stability: experimental
        """
        return self._values.get('handler')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'ServerlessApiProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


__all__ = [
    "ServerlessApi",
    "ServerlessApiProps",
]

publication.publish()
