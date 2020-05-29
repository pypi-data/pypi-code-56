# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import json
import warnings
import pulumi
import pulumi.runtime
from typing import Union
from . import utilities, tables

warnings.warn("rancher2.getRoleTempalte has been deprecated in favor of rancher2.getRoleTemplate", DeprecationWarning)
class GetRoleTempalteResult:
    """
    A collection of values returned by getRoleTempalte.
    """
    def __init__(__self__, administrative=None, annotations=None, builtin=None, context=None, default_role=None, description=None, external=None, hidden=None, id=None, labels=None, locked=None, name=None, role_template_ids=None, rules=None):
        if administrative and not isinstance(administrative, bool):
            raise TypeError("Expected argument 'administrative' to be a bool")
        __self__.administrative = administrative
        """
        (Computed) Administrative role template (bool)
        """
        if annotations and not isinstance(annotations, dict):
            raise TypeError("Expected argument 'annotations' to be a dict")
        __self__.annotations = annotations
        """
        (Computed) Annotations for role template object (map)
        """
        if builtin and not isinstance(builtin, bool):
            raise TypeError("Expected argument 'builtin' to be a bool")
        __self__.builtin = builtin
        """
        (Computed) Builtin role template (string)
        """
        if context and not isinstance(context, str):
            raise TypeError("Expected argument 'context' to be a str")
        __self__.context = context
        if default_role and not isinstance(default_role, bool):
            raise TypeError("Expected argument 'default_role' to be a bool")
        __self__.default_role = default_role
        """
        (Computed) Default role template for new created cluster or project (bool)
        """
        if description and not isinstance(description, str):
            raise TypeError("Expected argument 'description' to be a str")
        __self__.description = description
        """
        (Computed) Role template description (string)
        """
        if external and not isinstance(external, bool):
            raise TypeError("Expected argument 'external' to be a bool")
        __self__.external = external
        """
        (Computed) External role template (bool)
        """
        if hidden and not isinstance(hidden, bool):
            raise TypeError("Expected argument 'hidden' to be a bool")
        __self__.hidden = hidden
        """
        (Computed) Hidden role template (bool)
        """
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        __self__.id = id
        """
        The provider-assigned unique ID for this managed resource.
        """
        if labels and not isinstance(labels, dict):
            raise TypeError("Expected argument 'labels' to be a dict")
        __self__.labels = labels
        """
        (Computed) Labels for role template object (map)
        """
        if locked and not isinstance(locked, bool):
            raise TypeError("Expected argument 'locked' to be a bool")
        __self__.locked = locked
        """
        (Computed) Locked role template (bool)
        """
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        __self__.name = name
        if role_template_ids and not isinstance(role_template_ids, list):
            raise TypeError("Expected argument 'role_template_ids' to be a list")
        __self__.role_template_ids = role_template_ids
        """
        (Computed) Inherit role template IDs (list)
        """
        if rules and not isinstance(rules, list):
            raise TypeError("Expected argument 'rules' to be a list")
        __self__.rules = rules
        """
        (Computed) Role template policy rules (list)
        """
class AwaitableGetRoleTempalteResult(GetRoleTempalteResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetRoleTempalteResult(
            administrative=self.administrative,
            annotations=self.annotations,
            builtin=self.builtin,
            context=self.context,
            default_role=self.default_role,
            description=self.description,
            external=self.external,
            hidden=self.hidden,
            id=self.id,
            labels=self.labels,
            locked=self.locked,
            name=self.name,
            role_template_ids=self.role_template_ids,
            rules=self.rules)

def get_role_tempalte(context=None,name=None,opts=None):
    """
    Use this data source to retrieve information about a Rancher v2 role template resource.

    ## Example Usage



    ```python
    import pulumi
    import pulumi_rancher2 as rancher2

    foo = rancher2.get_role_template(name="foo")
    ```



    :param str context: Role template context. `cluster` and `project` values are supported (string)
    :param str name: The name of the Node Template (string)
    """
    pulumi.log.warn("get_role_tempalte is deprecated: rancher2.getRoleTempalte has been deprecated in favor of rancher2.getRoleTemplate")
    __args__ = dict()


    __args__['context'] = context
    __args__['name'] = name
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = utilities.get_version()
    __ret__ = pulumi.runtime.invoke('rancher2:index/getRoleTempalte:getRoleTempalte', __args__, opts=opts).value

    return AwaitableGetRoleTempalteResult(
        administrative=__ret__.get('administrative'),
        annotations=__ret__.get('annotations'),
        builtin=__ret__.get('builtin'),
        context=__ret__.get('context'),
        default_role=__ret__.get('defaultRole'),
        description=__ret__.get('description'),
        external=__ret__.get('external'),
        hidden=__ret__.get('hidden'),
        id=__ret__.get('id'),
        labels=__ret__.get('labels'),
        locked=__ret__.get('locked'),
        name=__ret__.get('name'),
        role_template_ids=__ret__.get('roleTemplateIds'),
        rules=__ret__.get('rules'))
