"""
# `cdk-github-import`

Import local file assets into a new GitHub repository

# Usage

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
from cdk_github_import import Deployment

# create a new github repository pahud/new-repo and import all files from ./lib to it
Deployment(stack, "NewImport",
    path="./lib",
    owner="pahud",
    repository_name="new-repo",
    access_token=cdk.SecretValue.secrets_manager("my-github-token",
        json_field="token"
    )
)
```

## Private repository

Set `visibility` to `PRIVATE` to create a private GitHub repository.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
visibility: RepositoryVisibility.PRIVATE,
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

import aws_cdk.aws_codestar
import aws_cdk.core


class Deployment(aws_cdk.core.Construct, metaclass=jsii.JSIIMeta, jsii_type="cdk-github-import.Deployment"):
    """
    stability
    :stability: experimental
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, access_token: aws_cdk.core.SecretValue, owner: str, path: str, repository_name: str, visibility: typing.Optional[aws_cdk.aws_codestar.RepositoryVisibility]=None) -> None:
        """
        :param scope: -
        :param id: -
        :param access_token: 
        :param owner: 
        :param path: 
        :param repository_name: 
        :param visibility: 

        stability
        :stability: experimental
        """
        props = DeploymentProps(access_token=access_token, owner=owner, path=path, repository_name=repository_name, visibility=visibility)

        jsii.create(Deployment, self, [scope, id, props])


@jsii.data_type(jsii_type="cdk-github-import.DeploymentProps", jsii_struct_bases=[], name_mapping={'access_token': 'accessToken', 'owner': 'owner', 'path': 'path', 'repository_name': 'repositoryName', 'visibility': 'visibility'})
class DeploymentProps():
    def __init__(self, *, access_token: aws_cdk.core.SecretValue, owner: str, path: str, repository_name: str, visibility: typing.Optional[aws_cdk.aws_codestar.RepositoryVisibility]=None) -> None:
        """
        :param access_token: 
        :param owner: 
        :param path: 
        :param repository_name: 
        :param visibility: 

        stability
        :stability: experimental
        """
        self._values = {
            'access_token': access_token,
            'owner': owner,
            'path': path,
            'repository_name': repository_name,
        }
        if visibility is not None: self._values["visibility"] = visibility

    @builtins.property
    def access_token(self) -> aws_cdk.core.SecretValue:
        """
        stability
        :stability: experimental
        """
        return self._values.get('access_token')

    @builtins.property
    def owner(self) -> str:
        """
        stability
        :stability: experimental
        """
        return self._values.get('owner')

    @builtins.property
    def path(self) -> str:
        """
        stability
        :stability: experimental
        """
        return self._values.get('path')

    @builtins.property
    def repository_name(self) -> str:
        """
        stability
        :stability: experimental
        """
        return self._values.get('repository_name')

    @builtins.property
    def visibility(self) -> typing.Optional[aws_cdk.aws_codestar.RepositoryVisibility]:
        """
        stability
        :stability: experimental
        """
        return self._values.get('visibility')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'DeploymentProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


__all__ = [
    "Deployment",
    "DeploymentProps",
]

publication.publish()
