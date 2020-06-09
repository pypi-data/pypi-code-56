"""
[![NPM version](https://badge.fury.io/js/cdk-serverless-api.svg)](https://badge.fury.io/js/cdk-serverless-api)
[![PyPI version](https://badge.fury.io/py/cdk-serverless-api.svg)](https://badge.fury.io/py/cdk-serverless-api)
![Release](https://github.com/pahud/serverless-api-demo/workflows/Release/badge.svg)

# Welcome to `cdk-serverless-api`

This sample construct library helps you build Serverless API in AWS.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
from cdk_serverless_api import ServerlessApi

ServerlessApi(self, "Api")
```
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
