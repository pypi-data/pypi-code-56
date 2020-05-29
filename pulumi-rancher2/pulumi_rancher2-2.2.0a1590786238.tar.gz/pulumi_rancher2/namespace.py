# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import json
import warnings
import pulumi
import pulumi.runtime
from typing import Union
from . import utilities, tables

class Namespace(pulumi.CustomResource):
    annotations: pulumi.Output[dict]
    """
    Annotations for Node Pool object (map)
    """
    container_resource_limit: pulumi.Output[dict]
    """
    Default containers resource limits on namespace (List maxitem:1)

      * `limitsCpu` (`str`) - Limit for limits cpu in namespace (string)
      * `limitsMemory` (`str`) - Limit for limits memory in namespace (string)
      * `requestsCpu` (`str`) - Limit for requests cpu in namespace (string)
      * `requestsMemory` (`str`) - Limit for requests memory in namespace (string)
    """
    description: pulumi.Output[str]
    """
    A namespace description (string)
    """
    labels: pulumi.Output[dict]
    """
    Labels for Node Pool object (map)
    """
    name: pulumi.Output[str]
    """
    The name of the namespace (string)
    """
    project_id: pulumi.Output[str]
    """
    The project id where assign namespace. It's on the form `project_id=<cluster_id>:<id>`. Updating `<id>` part on same `<cluster_id>` namespace will be moved between projects (string)
    """
    resource_quota: pulumi.Output[dict]
    """
    Resource quota for namespace. Rancher v2.1.x or higher (list maxitems:1)

      * `limit` (`dict`) - Resource quota limit for namespace (list maxitems:1)
        * `configMaps` (`str`) - Limit for config maps in namespace (string)
        * `limitsCpu` (`str`) - Limit for limits cpu in namespace (string)
        * `limitsMemory` (`str`) - Limit for limits memory in namespace (string)
        * `persistentVolumeClaims` (`str`) - Limit for persistent volume claims in namespace (string)
        * `pods` (`str`) - Limit for pods in namespace (string)
        * `replicationControllers` (`str`) - Limit for replication controllers in namespace (string)
        * `requestsCpu` (`str`) - Limit for requests cpu in namespace (string)
        * `requestsMemory` (`str`) - Limit for requests memory in namespace (string)
        * `requestsStorage` (`str`) - Limit for requests storage in namespace (string)
        * `secrets` (`str`) - Limit for secrets in namespace (string)
        * `services` (`str`)
        * `servicesLoadBalancers` (`str`) - Limit for services load balancers in namespace (string)
        * `servicesNodePorts` (`str`) - Limit for services node ports in namespace (string)
    """
    wait_for_cluster: pulumi.Output[bool]
    """
    Wait for cluster becomes active. Default `false` (bool)
    """
    def __init__(__self__, resource_name, opts=None, annotations=None, container_resource_limit=None, description=None, labels=None, name=None, project_id=None, resource_quota=None, wait_for_cluster=None, __props__=None, __name__=None, __opts__=None):
        """
        Provides a Rancher v2 Namespace resource. This can be used to create namespaces for Rancher v2 environments and retrieve their information.

        ## Example Usage



        ```python
        import pulumi
        import pulumi_rancher2 as rancher2

        # Create a new rancher2 Namespace
        foo = rancher2.Namespace("foo",
            container_resource_limit={
                "limitsCpu": "20m",
                "limitsMemory": "20Mi",
                "requestsCpu": "1m",
                "requestsMemory": "1Mi",
            },
            description="foo namespace",
            project_id="<PROJECT_ID>",
            resource_quota={
                "limit": {
                    "limitsCpu": "100m",
                    "limitsMemory": "100Mi",
                    "requestsStorage": "1Gi",
                },
            })
        ```


        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[dict] annotations: Annotations for Node Pool object (map)
        :param pulumi.Input[dict] container_resource_limit: Default containers resource limits on namespace (List maxitem:1)
        :param pulumi.Input[str] description: A namespace description (string)
        :param pulumi.Input[dict] labels: Labels for Node Pool object (map)
        :param pulumi.Input[str] name: The name of the namespace (string)
        :param pulumi.Input[str] project_id: The project id where assign namespace. It's on the form `project_id=<cluster_id>:<id>`. Updating `<id>` part on same `<cluster_id>` namespace will be moved between projects (string)
        :param pulumi.Input[dict] resource_quota: Resource quota for namespace. Rancher v2.1.x or higher (list maxitems:1)
        :param pulumi.Input[bool] wait_for_cluster: Wait for cluster becomes active. Default `false` (bool)

        The **container_resource_limit** object supports the following:

          * `limitsCpu` (`pulumi.Input[str]`) - Limit for limits cpu in namespace (string)
          * `limitsMemory` (`pulumi.Input[str]`) - Limit for limits memory in namespace (string)
          * `requestsCpu` (`pulumi.Input[str]`) - Limit for requests cpu in namespace (string)
          * `requestsMemory` (`pulumi.Input[str]`) - Limit for requests memory in namespace (string)

        The **resource_quota** object supports the following:

          * `limit` (`pulumi.Input[dict]`) - Resource quota limit for namespace (list maxitems:1)
            * `configMaps` (`pulumi.Input[str]`) - Limit for config maps in namespace (string)
            * `limitsCpu` (`pulumi.Input[str]`) - Limit for limits cpu in namespace (string)
            * `limitsMemory` (`pulumi.Input[str]`) - Limit for limits memory in namespace (string)
            * `persistentVolumeClaims` (`pulumi.Input[str]`) - Limit for persistent volume claims in namespace (string)
            * `pods` (`pulumi.Input[str]`) - Limit for pods in namespace (string)
            * `replicationControllers` (`pulumi.Input[str]`) - Limit for replication controllers in namespace (string)
            * `requestsCpu` (`pulumi.Input[str]`) - Limit for requests cpu in namespace (string)
            * `requestsMemory` (`pulumi.Input[str]`) - Limit for requests memory in namespace (string)
            * `requestsStorage` (`pulumi.Input[str]`) - Limit for requests storage in namespace (string)
            * `secrets` (`pulumi.Input[str]`) - Limit for secrets in namespace (string)
            * `services` (`pulumi.Input[str]`)
            * `servicesLoadBalancers` (`pulumi.Input[str]`) - Limit for services load balancers in namespace (string)
            * `servicesNodePorts` (`pulumi.Input[str]`) - Limit for services node ports in namespace (string)
        """
        if __name__ is not None:
            warnings.warn("explicit use of __name__ is deprecated", DeprecationWarning)
            resource_name = __name__
        if __opts__ is not None:
            warnings.warn("explicit use of __opts__ is deprecated, use 'opts' instead", DeprecationWarning)
            opts = __opts__
        if opts is None:
            opts = pulumi.ResourceOptions()
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.version is None:
            opts.version = utilities.get_version()
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = dict()

            __props__['annotations'] = annotations
            __props__['container_resource_limit'] = container_resource_limit
            __props__['description'] = description
            __props__['labels'] = labels
            __props__['name'] = name
            if project_id is None:
                raise TypeError("Missing required property 'project_id'")
            __props__['project_id'] = project_id
            __props__['resource_quota'] = resource_quota
            __props__['wait_for_cluster'] = wait_for_cluster
        super(Namespace, __self__).__init__(
            'rancher2:index/namespace:Namespace',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name, id, opts=None, annotations=None, container_resource_limit=None, description=None, labels=None, name=None, project_id=None, resource_quota=None, wait_for_cluster=None):
        """
        Get an existing Namespace resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param str id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[dict] annotations: Annotations for Node Pool object (map)
        :param pulumi.Input[dict] container_resource_limit: Default containers resource limits on namespace (List maxitem:1)
        :param pulumi.Input[str] description: A namespace description (string)
        :param pulumi.Input[dict] labels: Labels for Node Pool object (map)
        :param pulumi.Input[str] name: The name of the namespace (string)
        :param pulumi.Input[str] project_id: The project id where assign namespace. It's on the form `project_id=<cluster_id>:<id>`. Updating `<id>` part on same `<cluster_id>` namespace will be moved between projects (string)
        :param pulumi.Input[dict] resource_quota: Resource quota for namespace. Rancher v2.1.x or higher (list maxitems:1)
        :param pulumi.Input[bool] wait_for_cluster: Wait for cluster becomes active. Default `false` (bool)

        The **container_resource_limit** object supports the following:

          * `limitsCpu` (`pulumi.Input[str]`) - Limit for limits cpu in namespace (string)
          * `limitsMemory` (`pulumi.Input[str]`) - Limit for limits memory in namespace (string)
          * `requestsCpu` (`pulumi.Input[str]`) - Limit for requests cpu in namespace (string)
          * `requestsMemory` (`pulumi.Input[str]`) - Limit for requests memory in namespace (string)

        The **resource_quota** object supports the following:

          * `limit` (`pulumi.Input[dict]`) - Resource quota limit for namespace (list maxitems:1)
            * `configMaps` (`pulumi.Input[str]`) - Limit for config maps in namespace (string)
            * `limitsCpu` (`pulumi.Input[str]`) - Limit for limits cpu in namespace (string)
            * `limitsMemory` (`pulumi.Input[str]`) - Limit for limits memory in namespace (string)
            * `persistentVolumeClaims` (`pulumi.Input[str]`) - Limit for persistent volume claims in namespace (string)
            * `pods` (`pulumi.Input[str]`) - Limit for pods in namespace (string)
            * `replicationControllers` (`pulumi.Input[str]`) - Limit for replication controllers in namespace (string)
            * `requestsCpu` (`pulumi.Input[str]`) - Limit for requests cpu in namespace (string)
            * `requestsMemory` (`pulumi.Input[str]`) - Limit for requests memory in namespace (string)
            * `requestsStorage` (`pulumi.Input[str]`) - Limit for requests storage in namespace (string)
            * `secrets` (`pulumi.Input[str]`) - Limit for secrets in namespace (string)
            * `services` (`pulumi.Input[str]`)
            * `servicesLoadBalancers` (`pulumi.Input[str]`) - Limit for services load balancers in namespace (string)
            * `servicesNodePorts` (`pulumi.Input[str]`) - Limit for services node ports in namespace (string)
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        __props__["annotations"] = annotations
        __props__["container_resource_limit"] = container_resource_limit
        __props__["description"] = description
        __props__["labels"] = labels
        __props__["name"] = name
        __props__["project_id"] = project_id
        __props__["resource_quota"] = resource_quota
        __props__["wait_for_cluster"] = wait_for_cluster
        return Namespace(resource_name, opts=opts, __props__=__props__)
    def translate_output_property(self, prop):
        return tables._CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return tables._SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

