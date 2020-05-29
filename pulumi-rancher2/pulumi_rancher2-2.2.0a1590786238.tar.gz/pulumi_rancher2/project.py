# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import json
import warnings
import pulumi
import pulumi.runtime
from typing import Union
from . import utilities, tables

class Project(pulumi.CustomResource):
    annotations: pulumi.Output[dict]
    """
    Annotations for Node Pool object (map)
    """
    cluster_id: pulumi.Output[str]
    """
    The cluster id where create project (string)
    """
    container_resource_limit: pulumi.Output[dict]
    """
    Default containers resource limits on project (List maxitem:1)

      * `limitsCpu` (`str`) - Limit for limits cpu in project (string)
      * `limitsMemory` (`str`) - Limit for limits memory in project (string)
      * `requestsCpu` (`str`) - Limit for requests cpu in project (string)
      * `requestsMemory` (`str`) - Limit for requests memory in project (string)
    """
    description: pulumi.Output[str]
    """
    A project description (string)
    """
    enable_project_monitoring: pulumi.Output[bool]
    """
    Enable built-in project monitoring. Default `false` (bool)
    """
    labels: pulumi.Output[dict]
    """
    Labels for Node Pool object (map)
    """
    name: pulumi.Output[str]
    """
    The name of the project (string)
    """
    pod_security_policy_template_id: pulumi.Output[str]
    """
    Default Pod Security Policy ID for the project (string)
    """
    project_monitoring_input: pulumi.Output[dict]
    """
    Project monitoring config. Any parameter defined in [rancher-monitoring charts](https://github.com/rancher/system-charts/tree/dev/charts/rancher-monitoring) could be configured (list maxitems:1)

      * `answers` (`dict`) - Key/value answers for monitor input (map)
      * `version` (`str`) - rancher-monitoring chart version (string)
    """
    resource_quota: pulumi.Output[dict]
    """
    Resource quota for project. Rancher v2.1.x or higher (list maxitems:1)

      * `namespaceDefaultLimit` (`dict`) - Default resource quota limit for  namespaces in project (list maxitems:1)
        * `configMaps` (`str`) - Limit for config maps in project (string)
        * `limitsCpu` (`str`) - Limit for limits cpu in project (string)
        * `limitsMemory` (`str`) - Limit for limits memory in project (string)
        * `persistentVolumeClaims` (`str`) - Limit for persistent volume claims in project (string)
        * `pods` (`str`) - Limit for pods in project (string)
        * `replicationControllers` (`str`) - Limit for replication controllers in project (string)
        * `requestsCpu` (`str`) - Limit for requests cpu in project (string)
        * `requestsMemory` (`str`) - Limit for requests memory in project (string)
        * `requestsStorage` (`str`) - Limit for requests storage in project (string)
        * `secrets` (`str`) - Limit for secrets in project (string)
        * `services` (`str`)
        * `servicesLoadBalancers` (`str`) - Limit for services load balancers in project (string)
        * `servicesNodePorts` (`str`) - Limit for services node ports in project (string)

      * `projectLimit` (`dict`) - Resource quota limit for project (list maxitems:1)
        * `configMaps` (`str`) - Limit for config maps in project (string)
        * `limitsCpu` (`str`) - Limit for limits cpu in project (string)
        * `limitsMemory` (`str`) - Limit for limits memory in project (string)
        * `persistentVolumeClaims` (`str`) - Limit for persistent volume claims in project (string)
        * `pods` (`str`) - Limit for pods in project (string)
        * `replicationControllers` (`str`) - Limit for replication controllers in project (string)
        * `requestsCpu` (`str`) - Limit for requests cpu in project (string)
        * `requestsMemory` (`str`) - Limit for requests memory in project (string)
        * `requestsStorage` (`str`) - Limit for requests storage in project (string)
        * `secrets` (`str`) - Limit for secrets in project (string)
        * `services` (`str`)
        * `servicesLoadBalancers` (`str`) - Limit for services load balancers in project (string)
        * `servicesNodePorts` (`str`) - Limit for services node ports in project (string)
    """
    wait_for_cluster: pulumi.Output[bool]
    """
    Wait for cluster becomes active. Default `false` (bool)
    """
    def __init__(__self__, resource_name, opts=None, annotations=None, cluster_id=None, container_resource_limit=None, description=None, enable_project_monitoring=None, labels=None, name=None, pod_security_policy_template_id=None, project_monitoring_input=None, resource_quota=None, wait_for_cluster=None, __props__=None, __name__=None, __opts__=None):
        """
        Provides a Rancher v2 Project resource. This can be used to create projects for Rancher v2 environments and retrieve their information.

        ## Example Usage



        ```python
        import pulumi
        import pulumi_rancher2 as rancher2

        # Create a new rancher2 Project
        foo = rancher2.Project("foo",
            cluster_id="<CLUSTER_ID>",
            container_resource_limit={
                "limitsCpu": "20m",
                "limitsMemory": "20Mi",
                "requestsCpu": "1m",
                "requestsMemory": "1Mi",
            },
            resource_quota={
                "namespaceDefaultLimit": {
                    "limitsCpu": "2000m",
                    "limitsMemory": "500Mi",
                    "requestsStorage": "1Gi",
                },
                "projectLimit": {
                    "limitsCpu": "2000m",
                    "limitsMemory": "2000Mi",
                    "requestsStorage": "2Gi",
                },
            })
        ```


        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[dict] annotations: Annotations for Node Pool object (map)
        :param pulumi.Input[str] cluster_id: The cluster id where create project (string)
        :param pulumi.Input[dict] container_resource_limit: Default containers resource limits on project (List maxitem:1)
        :param pulumi.Input[str] description: A project description (string)
        :param pulumi.Input[bool] enable_project_monitoring: Enable built-in project monitoring. Default `false` (bool)
        :param pulumi.Input[dict] labels: Labels for Node Pool object (map)
        :param pulumi.Input[str] name: The name of the project (string)
        :param pulumi.Input[str] pod_security_policy_template_id: Default Pod Security Policy ID for the project (string)
        :param pulumi.Input[dict] project_monitoring_input: Project monitoring config. Any parameter defined in [rancher-monitoring charts](https://github.com/rancher/system-charts/tree/dev/charts/rancher-monitoring) could be configured (list maxitems:1)
        :param pulumi.Input[dict] resource_quota: Resource quota for project. Rancher v2.1.x or higher (list maxitems:1)
        :param pulumi.Input[bool] wait_for_cluster: Wait for cluster becomes active. Default `false` (bool)

        The **container_resource_limit** object supports the following:

          * `limitsCpu` (`pulumi.Input[str]`) - Limit for limits cpu in project (string)
          * `limitsMemory` (`pulumi.Input[str]`) - Limit for limits memory in project (string)
          * `requestsCpu` (`pulumi.Input[str]`) - Limit for requests cpu in project (string)
          * `requestsMemory` (`pulumi.Input[str]`) - Limit for requests memory in project (string)

        The **project_monitoring_input** object supports the following:

          * `answers` (`pulumi.Input[dict]`) - Key/value answers for monitor input (map)
          * `version` (`pulumi.Input[str]`) - rancher-monitoring chart version (string)

        The **resource_quota** object supports the following:

          * `namespaceDefaultLimit` (`pulumi.Input[dict]`) - Default resource quota limit for  namespaces in project (list maxitems:1)
            * `configMaps` (`pulumi.Input[str]`) - Limit for config maps in project (string)
            * `limitsCpu` (`pulumi.Input[str]`) - Limit for limits cpu in project (string)
            * `limitsMemory` (`pulumi.Input[str]`) - Limit for limits memory in project (string)
            * `persistentVolumeClaims` (`pulumi.Input[str]`) - Limit for persistent volume claims in project (string)
            * `pods` (`pulumi.Input[str]`) - Limit for pods in project (string)
            * `replicationControllers` (`pulumi.Input[str]`) - Limit for replication controllers in project (string)
            * `requestsCpu` (`pulumi.Input[str]`) - Limit for requests cpu in project (string)
            * `requestsMemory` (`pulumi.Input[str]`) - Limit for requests memory in project (string)
            * `requestsStorage` (`pulumi.Input[str]`) - Limit for requests storage in project (string)
            * `secrets` (`pulumi.Input[str]`) - Limit for secrets in project (string)
            * `services` (`pulumi.Input[str]`)
            * `servicesLoadBalancers` (`pulumi.Input[str]`) - Limit for services load balancers in project (string)
            * `servicesNodePorts` (`pulumi.Input[str]`) - Limit for services node ports in project (string)

          * `projectLimit` (`pulumi.Input[dict]`) - Resource quota limit for project (list maxitems:1)
            * `configMaps` (`pulumi.Input[str]`) - Limit for config maps in project (string)
            * `limitsCpu` (`pulumi.Input[str]`) - Limit for limits cpu in project (string)
            * `limitsMemory` (`pulumi.Input[str]`) - Limit for limits memory in project (string)
            * `persistentVolumeClaims` (`pulumi.Input[str]`) - Limit for persistent volume claims in project (string)
            * `pods` (`pulumi.Input[str]`) - Limit for pods in project (string)
            * `replicationControllers` (`pulumi.Input[str]`) - Limit for replication controllers in project (string)
            * `requestsCpu` (`pulumi.Input[str]`) - Limit for requests cpu in project (string)
            * `requestsMemory` (`pulumi.Input[str]`) - Limit for requests memory in project (string)
            * `requestsStorage` (`pulumi.Input[str]`) - Limit for requests storage in project (string)
            * `secrets` (`pulumi.Input[str]`) - Limit for secrets in project (string)
            * `services` (`pulumi.Input[str]`)
            * `servicesLoadBalancers` (`pulumi.Input[str]`) - Limit for services load balancers in project (string)
            * `servicesNodePorts` (`pulumi.Input[str]`) - Limit for services node ports in project (string)
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
            if cluster_id is None:
                raise TypeError("Missing required property 'cluster_id'")
            __props__['cluster_id'] = cluster_id
            __props__['container_resource_limit'] = container_resource_limit
            __props__['description'] = description
            __props__['enable_project_monitoring'] = enable_project_monitoring
            __props__['labels'] = labels
            __props__['name'] = name
            __props__['pod_security_policy_template_id'] = pod_security_policy_template_id
            __props__['project_monitoring_input'] = project_monitoring_input
            __props__['resource_quota'] = resource_quota
            __props__['wait_for_cluster'] = wait_for_cluster
        super(Project, __self__).__init__(
            'rancher2:index/project:Project',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name, id, opts=None, annotations=None, cluster_id=None, container_resource_limit=None, description=None, enable_project_monitoring=None, labels=None, name=None, pod_security_policy_template_id=None, project_monitoring_input=None, resource_quota=None, wait_for_cluster=None):
        """
        Get an existing Project resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param str id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[dict] annotations: Annotations for Node Pool object (map)
        :param pulumi.Input[str] cluster_id: The cluster id where create project (string)
        :param pulumi.Input[dict] container_resource_limit: Default containers resource limits on project (List maxitem:1)
        :param pulumi.Input[str] description: A project description (string)
        :param pulumi.Input[bool] enable_project_monitoring: Enable built-in project monitoring. Default `false` (bool)
        :param pulumi.Input[dict] labels: Labels for Node Pool object (map)
        :param pulumi.Input[str] name: The name of the project (string)
        :param pulumi.Input[str] pod_security_policy_template_id: Default Pod Security Policy ID for the project (string)
        :param pulumi.Input[dict] project_monitoring_input: Project monitoring config. Any parameter defined in [rancher-monitoring charts](https://github.com/rancher/system-charts/tree/dev/charts/rancher-monitoring) could be configured (list maxitems:1)
        :param pulumi.Input[dict] resource_quota: Resource quota for project. Rancher v2.1.x or higher (list maxitems:1)
        :param pulumi.Input[bool] wait_for_cluster: Wait for cluster becomes active. Default `false` (bool)

        The **container_resource_limit** object supports the following:

          * `limitsCpu` (`pulumi.Input[str]`) - Limit for limits cpu in project (string)
          * `limitsMemory` (`pulumi.Input[str]`) - Limit for limits memory in project (string)
          * `requestsCpu` (`pulumi.Input[str]`) - Limit for requests cpu in project (string)
          * `requestsMemory` (`pulumi.Input[str]`) - Limit for requests memory in project (string)

        The **project_monitoring_input** object supports the following:

          * `answers` (`pulumi.Input[dict]`) - Key/value answers for monitor input (map)
          * `version` (`pulumi.Input[str]`) - rancher-monitoring chart version (string)

        The **resource_quota** object supports the following:

          * `namespaceDefaultLimit` (`pulumi.Input[dict]`) - Default resource quota limit for  namespaces in project (list maxitems:1)
            * `configMaps` (`pulumi.Input[str]`) - Limit for config maps in project (string)
            * `limitsCpu` (`pulumi.Input[str]`) - Limit for limits cpu in project (string)
            * `limitsMemory` (`pulumi.Input[str]`) - Limit for limits memory in project (string)
            * `persistentVolumeClaims` (`pulumi.Input[str]`) - Limit for persistent volume claims in project (string)
            * `pods` (`pulumi.Input[str]`) - Limit for pods in project (string)
            * `replicationControllers` (`pulumi.Input[str]`) - Limit for replication controllers in project (string)
            * `requestsCpu` (`pulumi.Input[str]`) - Limit for requests cpu in project (string)
            * `requestsMemory` (`pulumi.Input[str]`) - Limit for requests memory in project (string)
            * `requestsStorage` (`pulumi.Input[str]`) - Limit for requests storage in project (string)
            * `secrets` (`pulumi.Input[str]`) - Limit for secrets in project (string)
            * `services` (`pulumi.Input[str]`)
            * `servicesLoadBalancers` (`pulumi.Input[str]`) - Limit for services load balancers in project (string)
            * `servicesNodePorts` (`pulumi.Input[str]`) - Limit for services node ports in project (string)

          * `projectLimit` (`pulumi.Input[dict]`) - Resource quota limit for project (list maxitems:1)
            * `configMaps` (`pulumi.Input[str]`) - Limit for config maps in project (string)
            * `limitsCpu` (`pulumi.Input[str]`) - Limit for limits cpu in project (string)
            * `limitsMemory` (`pulumi.Input[str]`) - Limit for limits memory in project (string)
            * `persistentVolumeClaims` (`pulumi.Input[str]`) - Limit for persistent volume claims in project (string)
            * `pods` (`pulumi.Input[str]`) - Limit for pods in project (string)
            * `replicationControllers` (`pulumi.Input[str]`) - Limit for replication controllers in project (string)
            * `requestsCpu` (`pulumi.Input[str]`) - Limit for requests cpu in project (string)
            * `requestsMemory` (`pulumi.Input[str]`) - Limit for requests memory in project (string)
            * `requestsStorage` (`pulumi.Input[str]`) - Limit for requests storage in project (string)
            * `secrets` (`pulumi.Input[str]`) - Limit for secrets in project (string)
            * `services` (`pulumi.Input[str]`)
            * `servicesLoadBalancers` (`pulumi.Input[str]`) - Limit for services load balancers in project (string)
            * `servicesNodePorts` (`pulumi.Input[str]`) - Limit for services node ports in project (string)
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        __props__["annotations"] = annotations
        __props__["cluster_id"] = cluster_id
        __props__["container_resource_limit"] = container_resource_limit
        __props__["description"] = description
        __props__["enable_project_monitoring"] = enable_project_monitoring
        __props__["labels"] = labels
        __props__["name"] = name
        __props__["pod_security_policy_template_id"] = pod_security_policy_template_id
        __props__["project_monitoring_input"] = project_monitoring_input
        __props__["resource_quota"] = resource_quota
        __props__["wait_for_cluster"] = wait_for_cluster
        return Project(resource_name, opts=opts, __props__=__props__)
    def translate_output_property(self, prop):
        return tables._CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return tables._SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

