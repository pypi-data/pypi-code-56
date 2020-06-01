"""
# `eks-spot-blocks`

[![NPM version](https://badge.fury.io/js/eks-spot-blocks.svg)](https://badge.fury.io/js/eks-spot-blocks)

`eks-spot-blocks` is a JSII construct library for AWS CDK which aims to help you provison Amazon EKS cluster with `EC2 Spot Blocks` for defined duration workloads and helps you benefit from ensured availability and considerable price reduction for your kubernetes workload.

![](images/pahud_eks-spot2.png)

## Features

* [x] support the upstream AWS CDK `aws-eks` construct libraries by extending its capabilities
* [x] `addSpotFleet()` to create your spot fleet for your cluster
* [x] define your `blockDuration`, `validFrom` and `validUntil` for fine-graned control
* [x] support any AWS commercial regions which has Amazon EKS and EC2 Spot Block support, including AWS China regions

## Sample

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
import eks_spot_blocks as eksspot
import aws_cdk.core as cdk
import aws_cdk.aws_ec2 as ec2

cluster_stack = eksspot.EksSpotCluster(stack, "Cluster",
    cluster_version=eksspot.ClusterVersion.KUBERNETES_116
)

cluster_stack.add_spot_fleet("FirstFleet",
    block_duration=eksspot.BlockDuration.SIX_HOURS,
    target_capacity=1,
    default_instance_type=ec2.InstanceType("p3.2xlarge"),
    valid_until=cluster_stack.add_hours(Date(), 6).to_iSOString(),
    terminate_instances_with_expiration=True
)

cluster_stack.add_spot_fleet("SecondFleet",
    block_duration=eksspot.BlockDuration.ONE_HOUR,
    target_capacity=2,
    default_instance_type=ec2.InstanceType("c5.large"),
    valid_until=cluster_stack.add_hours(Date(), 1).to_iSOString(),
    terminate_instances_with_expiration=True
)
```

check [eks-spot-blocks-demo](https://github.com/pahud/eks-spot-blocks-demo) for a full AWS CDK demo with this construct library.

## Custom AMI support

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
cluster_stack = EksSpotCluster(stack, "Cluster",
    cluster_version=ClusterVersion.KUBERNETES_116,
    custom_ami_id="ami-xxxxxx"
)
```

## FAQ

### Does `eks-spot-blocks` support existing eks clusters created by `eksctl`, `terraform` or any other tools?

No. This construct library does not support existing Amazon EKS clusters. You have to create the cluster as well as the spot fleet altogether in this construct library.

### Can I write the CDK in other languages like `Python` and `Java`?

Not at this moment. But we plan to publish this construct with `JSII` so we can install this library via `npm`, `pypi`, `maven` or `nuget`.

### How much time can I block the spotfleet?

You can block the fleet with hourly increments up to 6 hours.

### What happens after the `blockDuration`?

Spot Blocks ensure the availability of your spot instances during the `blockDuration` and avoid termination during the price disruption. After the `blockDuration`, by default, your spot instances will still be in `running` state but it doesn't ensure the availability, which means it might be terminated anytime after the `blockDuration`.

### Can I terminate the fleet immediately after the `blockDuration` to save the money?

Yes. Basically you can configure `validFrom`, `validUntil` and `terminateInstancesWithExpiration` to achieve this.

However, consider the following scenario

```
<deploy start at 1:00>|--------(one hour)-----------------------|<2:00>
                           |<fleet created at 1:05>--------(one-hour block)-------|<2:05>
```

Your fleet will be terminated at `2:00` rather at `2:05`.

### Are `tains` and `labels` supported?

Yes.

(samples TBD)

### Does it support AWS China regions?

Yes. Including **Beijing**(`cn-north-1`) and **Ningxia**(`cn-northwest-1`).

### How much can I save from the EC2 Spot Block compared to the on-demand?

According to this [document](https://aws.amazon.com/ec2/spot/pricing/?nc1=h_ls)

`Spot Instances are also available to run for a predefined duration – in hourly increments up to six hours in length – at a discount of up to 30-50% compared to On-Demand pricing.`

### Will this library become part of the upstream `aws-eks` construct library?

Probably. As it's still in the preliminary stage, we are still collecting feedbacks from the community to make `eks-spot-blocks` ready for production workloads. Eventually we will commit this feature to the upstream `aws-eks` construct library in AWS CDK through pull requests.
"""
import abc
import builtins
import datetime
import enum
import typing

import jsii
import jsii.compat
import publication

import aws_cdk.aws_ec2
import aws_cdk.aws_eks
import aws_cdk.aws_iam
import aws_cdk.aws_ssm
import aws_cdk.core
import constructs

from ._jsii import *


@jsii.data_type(jsii_type="eks-spot-blocks.BaseSpotFleetProps", jsii_struct_bases=[aws_cdk.core.ResourceProps], name_mapping={'physical_name': 'physicalName', 'block_duration': 'blockDuration', 'bootstrap_enabled': 'bootstrapEnabled', 'custom_ami_id': 'customAmiId', 'default_instance_type': 'defaultInstanceType', 'instance_interruption_behavior': 'instanceInterruptionBehavior', 'instance_role': 'instanceRole', 'map_role': 'mapRole', 'target_capacity': 'targetCapacity', 'terminate_instances_with_expiration': 'terminateInstancesWithExpiration', 'valid_from': 'validFrom', 'valid_until': 'validUntil'})
class BaseSpotFleetProps(aws_cdk.core.ResourceProps):
    def __init__(self, *, physical_name: typing.Optional[str]=None, block_duration: typing.Optional["BlockDuration"]=None, bootstrap_enabled: typing.Optional[bool]=None, custom_ami_id: typing.Optional[str]=None, default_instance_type: typing.Optional[aws_cdk.aws_ec2.InstanceType]=None, instance_interruption_behavior: typing.Optional["InstanceInterruptionBehavior"]=None, instance_role: typing.Optional[aws_cdk.aws_iam.Role]=None, map_role: typing.Optional[bool]=None, target_capacity: typing.Optional[jsii.Number]=None, terminate_instances_with_expiration: typing.Optional[bool]=None, valid_from: typing.Optional[str]=None, valid_until: typing.Optional[str]=None) -> None:
        """
        :param physical_name: The value passed in by users to the physical name prop of the resource. - ``undefined`` implies that a physical name will be allocated by CloudFormation during deployment. - a concrete value implies a specific physical name - ``PhysicalName.GENERATE_IF_NEEDED`` is a marker that indicates that a physical will only be generated by the CDK if it is needed for cross-environment references. Otherwise, it will be allocated by CloudFormation. Default: - The physical name will be allocated by CloudFormation at deployment time
        :param block_duration: -
        :param bootstrap_enabled: -
        :param custom_ami_id: -
        :param default_instance_type: -
        :param instance_interruption_behavior: -
        :param instance_role: -
        :param map_role: -
        :param target_capacity: -
        :param terminate_instances_with_expiration: -
        :param valid_from: -
        :param valid_until: -
        """
        self._values = {
        }
        if physical_name is not None: self._values["physical_name"] = physical_name
        if block_duration is not None: self._values["block_duration"] = block_duration
        if bootstrap_enabled is not None: self._values["bootstrap_enabled"] = bootstrap_enabled
        if custom_ami_id is not None: self._values["custom_ami_id"] = custom_ami_id
        if default_instance_type is not None: self._values["default_instance_type"] = default_instance_type
        if instance_interruption_behavior is not None: self._values["instance_interruption_behavior"] = instance_interruption_behavior
        if instance_role is not None: self._values["instance_role"] = instance_role
        if map_role is not None: self._values["map_role"] = map_role
        if target_capacity is not None: self._values["target_capacity"] = target_capacity
        if terminate_instances_with_expiration is not None: self._values["terminate_instances_with_expiration"] = terminate_instances_with_expiration
        if valid_from is not None: self._values["valid_from"] = valid_from
        if valid_until is not None: self._values["valid_until"] = valid_until

    @builtins.property
    def physical_name(self) -> typing.Optional[str]:
        """The value passed in by users to the physical name prop of the resource.

        - ``undefined`` implies that a physical name will be allocated by
          CloudFormation during deployment.
        - a concrete value implies a specific physical name
        - ``PhysicalName.GENERATE_IF_NEEDED`` is a marker that indicates that a physical will only be generated
          by the CDK if it is needed for cross-environment references. Otherwise, it will be allocated by CloudFormation.

        default
        :default: - The physical name will be allocated by CloudFormation at deployment time
        """
        return self._values.get('physical_name')

    @builtins.property
    def block_duration(self) -> typing.Optional["BlockDuration"]:
        return self._values.get('block_duration')

    @builtins.property
    def bootstrap_enabled(self) -> typing.Optional[bool]:
        return self._values.get('bootstrap_enabled')

    @builtins.property
    def custom_ami_id(self) -> typing.Optional[str]:
        return self._values.get('custom_ami_id')

    @builtins.property
    def default_instance_type(self) -> typing.Optional[aws_cdk.aws_ec2.InstanceType]:
        return self._values.get('default_instance_type')

    @builtins.property
    def instance_interruption_behavior(self) -> typing.Optional["InstanceInterruptionBehavior"]:
        return self._values.get('instance_interruption_behavior')

    @builtins.property
    def instance_role(self) -> typing.Optional[aws_cdk.aws_iam.Role]:
        return self._values.get('instance_role')

    @builtins.property
    def map_role(self) -> typing.Optional[bool]:
        return self._values.get('map_role')

    @builtins.property
    def target_capacity(self) -> typing.Optional[jsii.Number]:
        return self._values.get('target_capacity')

    @builtins.property
    def terminate_instances_with_expiration(self) -> typing.Optional[bool]:
        return self._values.get('terminate_instances_with_expiration')

    @builtins.property
    def valid_from(self) -> typing.Optional[str]:
        return self._values.get('valid_from')

    @builtins.property
    def valid_until(self) -> typing.Optional[str]:
        return self._values.get('valid_until')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'BaseSpotFleetProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.enum(jsii_type="eks-spot-blocks.BlockDuration")
class BlockDuration(enum.Enum):
    ONE_HOUR = "ONE_HOUR"
    TWO_HOURS = "TWO_HOURS"
    THREE_HOURS = "THREE_HOURS"
    FOUR_HOURS = "FOUR_HOURS"
    FIVE_HOURS = "FIVE_HOURS"
    SIX_HOURS = "SIX_HOURS"

@jsii.enum(jsii_type="eks-spot-blocks.ClusterVersion")
class ClusterVersion(enum.Enum):
    KUBERNETES_114 = "KUBERNETES_114"
    KUBERNETES_115 = "KUBERNETES_115"
    KUBERNETES_116 = "KUBERNETES_116"

class EksSpotCluster(aws_cdk.core.Resource, metaclass=jsii.JSIIMeta, jsii_type="eks-spot-blocks.EksSpotCluster"):
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, cluster_version: "ClusterVersion", cluster_attributes: typing.Optional[aws_cdk.aws_eks.ClusterAttributes]=None, custom_ami_id: typing.Optional[str]=None, instance_interruption_behavior: typing.Optional["InstanceInterruptionBehavior"]=None, instance_role: typing.Optional[aws_cdk.aws_iam.IRole]=None, kubectl_enabled: typing.Optional[bool]=None, description: typing.Optional[str]=None, env: typing.Optional[aws_cdk.core.Environment]=None, stack_name: typing.Optional[str]=None, synthesizer: typing.Optional[aws_cdk.core.IStackSynthesizer]=None, tags: typing.Optional[typing.Mapping[str, str]]=None, termination_protection: typing.Optional[bool]=None) -> None:
        """
        :param scope: -
        :param id: -
        :param cluster_version: -
        :param cluster_attributes: -
        :param custom_ami_id: Specify a custom AMI ID for your spot fleet. By default the Amazon EKS-optimized AMI will be selected. Default: - none
        :param instance_interruption_behavior: -
        :param instance_role: -
        :param kubectl_enabled: -
        :param description: A description of the stack. Default: - No description.
        :param env: The AWS environment (account/region) where this stack will be deployed. Default: - The ``default-account`` and ``default-region`` context parameters will be used. If they are undefined, it will not be possible to deploy the stack.
        :param stack_name: Name to deploy the stack with. Default: - Derived from construct path.
        :param synthesizer: Synthesis method to use while deploying this stack. Default: - ``DefaultStackSynthesizer`` if the ``@aws-cdk/core:newStyleStackSynthesis`` feature flag is set, ``LegacyStackSynthesizer`` otherwise.
        :param tags: Stack tags that will be applied to all the taggable resources and the stack itself. Default: {}
        :param termination_protection: Whether to enable termination protection for this stack. Default: false
        """
        props = EksSpotClusterProps(cluster_version=cluster_version, cluster_attributes=cluster_attributes, custom_ami_id=custom_ami_id, instance_interruption_behavior=instance_interruption_behavior, instance_role=instance_role, kubectl_enabled=kubectl_enabled, description=description, env=env, stack_name=stack_name, synthesizer=synthesizer, tags=tags, termination_protection=termination_protection)

        jsii.create(EksSpotCluster, self, [scope, id, props])

    @jsii.member(jsii_name="addDays")
    def add_days(self, date: datetime.datetime, days: jsii.Number) -> datetime.datetime:
        """
        :param date: -
        :param days: -
        """
        return jsii.invoke(self, "addDays", [date, days])

    @jsii.member(jsii_name="addHours")
    def add_hours(self, date: datetime.datetime, hours: jsii.Number) -> datetime.datetime:
        """
        :param date: -
        :param hours: -
        """
        return jsii.invoke(self, "addHours", [date, hours])

    @jsii.member(jsii_name="addMinutes")
    def add_minutes(self, date: datetime.datetime, minutes: jsii.Number) -> datetime.datetime:
        """
        :param date: -
        :param minutes: -
        """
        return jsii.invoke(self, "addMinutes", [date, minutes])

    @jsii.member(jsii_name="addSpotFleet")
    def add_spot_fleet(self, id: str, *, block_duration: typing.Optional["BlockDuration"]=None, bootstrap_enabled: typing.Optional[bool]=None, custom_ami_id: typing.Optional[str]=None, default_instance_type: typing.Optional[aws_cdk.aws_ec2.InstanceType]=None, instance_interruption_behavior: typing.Optional["InstanceInterruptionBehavior"]=None, instance_role: typing.Optional[aws_cdk.aws_iam.Role]=None, map_role: typing.Optional[bool]=None, target_capacity: typing.Optional[jsii.Number]=None, terminate_instances_with_expiration: typing.Optional[bool]=None, valid_from: typing.Optional[str]=None, valid_until: typing.Optional[str]=None, physical_name: typing.Optional[str]=None) -> None:
        """
        :param id: -
        :param block_duration: -
        :param bootstrap_enabled: -
        :param custom_ami_id: -
        :param default_instance_type: -
        :param instance_interruption_behavior: -
        :param instance_role: -
        :param map_role: -
        :param target_capacity: -
        :param terminate_instances_with_expiration: -
        :param valid_from: -
        :param valid_until: -
        :param physical_name: The value passed in by users to the physical name prop of the resource. - ``undefined`` implies that a physical name will be allocated by CloudFormation during deployment. - a concrete value implies a specific physical name - ``PhysicalName.GENERATE_IF_NEEDED`` is a marker that indicates that a physical will only be generated by the CDK if it is needed for cross-environment references. Otherwise, it will be allocated by CloudFormation. Default: - The physical name will be allocated by CloudFormation at deployment time
        """
        props = BaseSpotFleetProps(block_duration=block_duration, bootstrap_enabled=bootstrap_enabled, custom_ami_id=custom_ami_id, default_instance_type=default_instance_type, instance_interruption_behavior=instance_interruption_behavior, instance_role=instance_role, map_role=map_role, target_capacity=target_capacity, terminate_instances_with_expiration=terminate_instances_with_expiration, valid_from=valid_from, valid_until=valid_until, physical_name=physical_name)

        return jsii.invoke(self, "addSpotFleet", [id, props])

    @builtins.property
    @jsii.member(jsii_name="cluster")
    def cluster(self) -> aws_cdk.aws_eks.Cluster:
        return jsii.get(self, "cluster")

    @builtins.property
    @jsii.member(jsii_name="clusterVersion")
    def cluster_version(self) -> "ClusterVersion":
        return jsii.get(self, "clusterVersion")

    @builtins.property
    @jsii.member(jsii_name="vpc")
    def vpc(self) -> aws_cdk.aws_ec2.IVpc:
        return jsii.get(self, "vpc")


@jsii.data_type(jsii_type="eks-spot-blocks.EksSpotClusterProps", jsii_struct_bases=[aws_cdk.core.StackProps], name_mapping={'description': 'description', 'env': 'env', 'stack_name': 'stackName', 'synthesizer': 'synthesizer', 'tags': 'tags', 'termination_protection': 'terminationProtection', 'cluster_version': 'clusterVersion', 'cluster_attributes': 'clusterAttributes', 'custom_ami_id': 'customAmiId', 'instance_interruption_behavior': 'instanceInterruptionBehavior', 'instance_role': 'instanceRole', 'kubectl_enabled': 'kubectlEnabled'})
class EksSpotClusterProps(aws_cdk.core.StackProps):
    def __init__(self, *, description: typing.Optional[str]=None, env: typing.Optional[aws_cdk.core.Environment]=None, stack_name: typing.Optional[str]=None, synthesizer: typing.Optional[aws_cdk.core.IStackSynthesizer]=None, tags: typing.Optional[typing.Mapping[str, str]]=None, termination_protection: typing.Optional[bool]=None, cluster_version: "ClusterVersion", cluster_attributes: typing.Optional[aws_cdk.aws_eks.ClusterAttributes]=None, custom_ami_id: typing.Optional[str]=None, instance_interruption_behavior: typing.Optional["InstanceInterruptionBehavior"]=None, instance_role: typing.Optional[aws_cdk.aws_iam.IRole]=None, kubectl_enabled: typing.Optional[bool]=None) -> None:
        """
        :param description: A description of the stack. Default: - No description.
        :param env: The AWS environment (account/region) where this stack will be deployed. Default: - The ``default-account`` and ``default-region`` context parameters will be used. If they are undefined, it will not be possible to deploy the stack.
        :param stack_name: Name to deploy the stack with. Default: - Derived from construct path.
        :param synthesizer: Synthesis method to use while deploying this stack. Default: - ``DefaultStackSynthesizer`` if the ``@aws-cdk/core:newStyleStackSynthesis`` feature flag is set, ``LegacyStackSynthesizer`` otherwise.
        :param tags: Stack tags that will be applied to all the taggable resources and the stack itself. Default: {}
        :param termination_protection: Whether to enable termination protection for this stack. Default: false
        :param cluster_version: -
        :param cluster_attributes: -
        :param custom_ami_id: Specify a custom AMI ID for your spot fleet. By default the Amazon EKS-optimized AMI will be selected. Default: - none
        :param instance_interruption_behavior: -
        :param instance_role: -
        :param kubectl_enabled: -
        """
        if isinstance(env, dict): env = aws_cdk.core.Environment(**env)
        if isinstance(cluster_attributes, dict): cluster_attributes = aws_cdk.aws_eks.ClusterAttributes(**cluster_attributes)
        self._values = {
            'cluster_version': cluster_version,
        }
        if description is not None: self._values["description"] = description
        if env is not None: self._values["env"] = env
        if stack_name is not None: self._values["stack_name"] = stack_name
        if synthesizer is not None: self._values["synthesizer"] = synthesizer
        if tags is not None: self._values["tags"] = tags
        if termination_protection is not None: self._values["termination_protection"] = termination_protection
        if cluster_attributes is not None: self._values["cluster_attributes"] = cluster_attributes
        if custom_ami_id is not None: self._values["custom_ami_id"] = custom_ami_id
        if instance_interruption_behavior is not None: self._values["instance_interruption_behavior"] = instance_interruption_behavior
        if instance_role is not None: self._values["instance_role"] = instance_role
        if kubectl_enabled is not None: self._values["kubectl_enabled"] = kubectl_enabled

    @builtins.property
    def description(self) -> typing.Optional[str]:
        """A description of the stack.

        default
        :default: - No description.
        """
        return self._values.get('description')

    @builtins.property
    def env(self) -> typing.Optional[aws_cdk.core.Environment]:
        """The AWS environment (account/region) where this stack will be deployed.

        default
        :default:

        - The ``default-account`` and ``default-region`` context parameters will be
          used. If they are undefined, it will not be possible to deploy the stack.
        """
        return self._values.get('env')

    @builtins.property
    def stack_name(self) -> typing.Optional[str]:
        """Name to deploy the stack with.

        default
        :default: - Derived from construct path.
        """
        return self._values.get('stack_name')

    @builtins.property
    def synthesizer(self) -> typing.Optional[aws_cdk.core.IStackSynthesizer]:
        """Synthesis method to use while deploying this stack.

        default
        :default:

        - ``DefaultStackSynthesizer`` if the ``@aws-cdk/core:newStyleStackSynthesis`` feature flag
          is set, ``LegacyStackSynthesizer`` otherwise.
        """
        return self._values.get('synthesizer')

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[str, str]]:
        """Stack tags that will be applied to all the taggable resources and the stack itself.

        default
        :default: {}
        """
        return self._values.get('tags')

    @builtins.property
    def termination_protection(self) -> typing.Optional[bool]:
        """Whether to enable termination protection for this stack.

        default
        :default: false
        """
        return self._values.get('termination_protection')

    @builtins.property
    def cluster_version(self) -> "ClusterVersion":
        return self._values.get('cluster_version')

    @builtins.property
    def cluster_attributes(self) -> typing.Optional[aws_cdk.aws_eks.ClusterAttributes]:
        return self._values.get('cluster_attributes')

    @builtins.property
    def custom_ami_id(self) -> typing.Optional[str]:
        """Specify a custom AMI ID for your spot fleet.

        By default the Amazon EKS-optimized
        AMI will be selected.

        default
        :default: - none
        """
        return self._values.get('custom_ami_id')

    @builtins.property
    def instance_interruption_behavior(self) -> typing.Optional["InstanceInterruptionBehavior"]:
        return self._values.get('instance_interruption_behavior')

    @builtins.property
    def instance_role(self) -> typing.Optional[aws_cdk.aws_iam.IRole]:
        return self._values.get('instance_role')

    @builtins.property
    def kubectl_enabled(self) -> typing.Optional[bool]:
        return self._values.get('kubectl_enabled')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'EksSpotClusterProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.interface(jsii_type="eks-spot-blocks.ILaunchtemplate")
class ILaunchtemplate(jsii.compat.Protocol):
    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _ILaunchtemplateProxy

    @jsii.member(jsii_name="bind")
    def bind(self, spotfleet: "SpotFleet") -> "SpotFleetLaunchTemplateConfig":
        """
        :param spotfleet: -
        """
        ...


class _ILaunchtemplateProxy():
    __jsii_type__ = "eks-spot-blocks.ILaunchtemplate"
    @jsii.member(jsii_name="bind")
    def bind(self, spotfleet: "SpotFleet") -> "SpotFleetLaunchTemplateConfig":
        """
        :param spotfleet: -
        """
        return jsii.invoke(self, "bind", [spotfleet])


@jsii.enum(jsii_type="eks-spot-blocks.InstanceInterruptionBehavior")
class InstanceInterruptionBehavior(enum.Enum):
    HIBERNATE = "HIBERNATE"
    STOP = "STOP"
    TERMINATE = "TERMINATE"

@jsii.implements(ILaunchtemplate)
class LaunchTemplate(metaclass=jsii.JSIIMeta, jsii_type="eks-spot-blocks.LaunchTemplate"):
    def __init__(self) -> None:
        jsii.create(LaunchTemplate, self, [])

    @jsii.member(jsii_name="bind")
    def bind(self, spotfleet: "SpotFleet") -> "SpotFleetLaunchTemplateConfig":
        """
        :param spotfleet: -
        """
        return jsii.invoke(self, "bind", [spotfleet])


class SpotFleet(aws_cdk.core.Resource, metaclass=jsii.JSIIMeta, jsii_type="eks-spot-blocks.SpotFleet"):
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, cluster: "EksSpotCluster", launch_template: typing.Optional["ILaunchtemplate"]=None, block_duration: typing.Optional["BlockDuration"]=None, bootstrap_enabled: typing.Optional[bool]=None, custom_ami_id: typing.Optional[str]=None, default_instance_type: typing.Optional[aws_cdk.aws_ec2.InstanceType]=None, instance_interruption_behavior: typing.Optional["InstanceInterruptionBehavior"]=None, instance_role: typing.Optional[aws_cdk.aws_iam.Role]=None, map_role: typing.Optional[bool]=None, target_capacity: typing.Optional[jsii.Number]=None, terminate_instances_with_expiration: typing.Optional[bool]=None, valid_from: typing.Optional[str]=None, valid_until: typing.Optional[str]=None, physical_name: typing.Optional[str]=None) -> None:
        """
        :param scope: -
        :param id: -
        :param cluster: -
        :param launch_template: -
        :param block_duration: -
        :param bootstrap_enabled: -
        :param custom_ami_id: -
        :param default_instance_type: -
        :param instance_interruption_behavior: -
        :param instance_role: -
        :param map_role: -
        :param target_capacity: -
        :param terminate_instances_with_expiration: -
        :param valid_from: -
        :param valid_until: -
        :param physical_name: The value passed in by users to the physical name prop of the resource. - ``undefined`` implies that a physical name will be allocated by CloudFormation during deployment. - a concrete value implies a specific physical name - ``PhysicalName.GENERATE_IF_NEEDED`` is a marker that indicates that a physical will only be generated by the CDK if it is needed for cross-environment references. Otherwise, it will be allocated by CloudFormation. Default: - The physical name will be allocated by CloudFormation at deployment time
        """
        props = SpotFleetProps(cluster=cluster, launch_template=launch_template, block_duration=block_duration, bootstrap_enabled=bootstrap_enabled, custom_ami_id=custom_ami_id, default_instance_type=default_instance_type, instance_interruption_behavior=instance_interruption_behavior, instance_role=instance_role, map_role=map_role, target_capacity=target_capacity, terminate_instances_with_expiration=terminate_instances_with_expiration, valid_from=valid_from, valid_until=valid_until, physical_name=physical_name)

        jsii.create(SpotFleet, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="clusterStack")
    def cluster_stack(self) -> "EksSpotCluster":
        return jsii.get(self, "clusterStack")

    @builtins.property
    @jsii.member(jsii_name="defaultInstanceType")
    def default_instance_type(self) -> aws_cdk.aws_ec2.InstanceType:
        return jsii.get(self, "defaultInstanceType")

    @builtins.property
    @jsii.member(jsii_name="instanceRole")
    def instance_role(self) -> aws_cdk.aws_iam.IRole:
        return jsii.get(self, "instanceRole")

    @builtins.property
    @jsii.member(jsii_name="launchTemplate")
    def launch_template(self) -> "ILaunchtemplate":
        return jsii.get(self, "launchTemplate")

    @builtins.property
    @jsii.member(jsii_name="spotFleetId")
    def spot_fleet_id(self) -> str:
        return jsii.get(self, "spotFleetId")

    @builtins.property
    @jsii.member(jsii_name="targetCapacity")
    def target_capacity(self) -> typing.Optional[jsii.Number]:
        return jsii.get(self, "targetCapacity")


@jsii.data_type(jsii_type="eks-spot-blocks.SpotFleetLaunchTemplateConfig", jsii_struct_bases=[], name_mapping={'launch_template': 'launchTemplate', 'spotfleet': 'spotfleet'})
class SpotFleetLaunchTemplateConfig():
    def __init__(self, *, launch_template: "ILaunchtemplate", spotfleet: "SpotFleet") -> None:
        """
        :param launch_template: -
        :param spotfleet: -
        """
        self._values = {
            'launch_template': launch_template,
            'spotfleet': spotfleet,
        }

    @builtins.property
    def launch_template(self) -> "ILaunchtemplate":
        return self._values.get('launch_template')

    @builtins.property
    def spotfleet(self) -> "SpotFleet":
        return self._values.get('spotfleet')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'SpotFleetLaunchTemplateConfig(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="eks-spot-blocks.SpotFleetProps", jsii_struct_bases=[BaseSpotFleetProps], name_mapping={'physical_name': 'physicalName', 'block_duration': 'blockDuration', 'bootstrap_enabled': 'bootstrapEnabled', 'custom_ami_id': 'customAmiId', 'default_instance_type': 'defaultInstanceType', 'instance_interruption_behavior': 'instanceInterruptionBehavior', 'instance_role': 'instanceRole', 'map_role': 'mapRole', 'target_capacity': 'targetCapacity', 'terminate_instances_with_expiration': 'terminateInstancesWithExpiration', 'valid_from': 'validFrom', 'valid_until': 'validUntil', 'cluster': 'cluster', 'launch_template': 'launchTemplate'})
class SpotFleetProps(BaseSpotFleetProps):
    def __init__(self, *, physical_name: typing.Optional[str]=None, block_duration: typing.Optional["BlockDuration"]=None, bootstrap_enabled: typing.Optional[bool]=None, custom_ami_id: typing.Optional[str]=None, default_instance_type: typing.Optional[aws_cdk.aws_ec2.InstanceType]=None, instance_interruption_behavior: typing.Optional["InstanceInterruptionBehavior"]=None, instance_role: typing.Optional[aws_cdk.aws_iam.Role]=None, map_role: typing.Optional[bool]=None, target_capacity: typing.Optional[jsii.Number]=None, terminate_instances_with_expiration: typing.Optional[bool]=None, valid_from: typing.Optional[str]=None, valid_until: typing.Optional[str]=None, cluster: "EksSpotCluster", launch_template: typing.Optional["ILaunchtemplate"]=None) -> None:
        """
        :param physical_name: The value passed in by users to the physical name prop of the resource. - ``undefined`` implies that a physical name will be allocated by CloudFormation during deployment. - a concrete value implies a specific physical name - ``PhysicalName.GENERATE_IF_NEEDED`` is a marker that indicates that a physical will only be generated by the CDK if it is needed for cross-environment references. Otherwise, it will be allocated by CloudFormation. Default: - The physical name will be allocated by CloudFormation at deployment time
        :param block_duration: -
        :param bootstrap_enabled: -
        :param custom_ami_id: -
        :param default_instance_type: -
        :param instance_interruption_behavior: -
        :param instance_role: -
        :param map_role: -
        :param target_capacity: -
        :param terminate_instances_with_expiration: -
        :param valid_from: -
        :param valid_until: -
        :param cluster: -
        :param launch_template: -
        """
        self._values = {
            'cluster': cluster,
        }
        if physical_name is not None: self._values["physical_name"] = physical_name
        if block_duration is not None: self._values["block_duration"] = block_duration
        if bootstrap_enabled is not None: self._values["bootstrap_enabled"] = bootstrap_enabled
        if custom_ami_id is not None: self._values["custom_ami_id"] = custom_ami_id
        if default_instance_type is not None: self._values["default_instance_type"] = default_instance_type
        if instance_interruption_behavior is not None: self._values["instance_interruption_behavior"] = instance_interruption_behavior
        if instance_role is not None: self._values["instance_role"] = instance_role
        if map_role is not None: self._values["map_role"] = map_role
        if target_capacity is not None: self._values["target_capacity"] = target_capacity
        if terminate_instances_with_expiration is not None: self._values["terminate_instances_with_expiration"] = terminate_instances_with_expiration
        if valid_from is not None: self._values["valid_from"] = valid_from
        if valid_until is not None: self._values["valid_until"] = valid_until
        if launch_template is not None: self._values["launch_template"] = launch_template

    @builtins.property
    def physical_name(self) -> typing.Optional[str]:
        """The value passed in by users to the physical name prop of the resource.

        - ``undefined`` implies that a physical name will be allocated by
          CloudFormation during deployment.
        - a concrete value implies a specific physical name
        - ``PhysicalName.GENERATE_IF_NEEDED`` is a marker that indicates that a physical will only be generated
          by the CDK if it is needed for cross-environment references. Otherwise, it will be allocated by CloudFormation.

        default
        :default: - The physical name will be allocated by CloudFormation at deployment time
        """
        return self._values.get('physical_name')

    @builtins.property
    def block_duration(self) -> typing.Optional["BlockDuration"]:
        return self._values.get('block_duration')

    @builtins.property
    def bootstrap_enabled(self) -> typing.Optional[bool]:
        return self._values.get('bootstrap_enabled')

    @builtins.property
    def custom_ami_id(self) -> typing.Optional[str]:
        return self._values.get('custom_ami_id')

    @builtins.property
    def default_instance_type(self) -> typing.Optional[aws_cdk.aws_ec2.InstanceType]:
        return self._values.get('default_instance_type')

    @builtins.property
    def instance_interruption_behavior(self) -> typing.Optional["InstanceInterruptionBehavior"]:
        return self._values.get('instance_interruption_behavior')

    @builtins.property
    def instance_role(self) -> typing.Optional[aws_cdk.aws_iam.Role]:
        return self._values.get('instance_role')

    @builtins.property
    def map_role(self) -> typing.Optional[bool]:
        return self._values.get('map_role')

    @builtins.property
    def target_capacity(self) -> typing.Optional[jsii.Number]:
        return self._values.get('target_capacity')

    @builtins.property
    def terminate_instances_with_expiration(self) -> typing.Optional[bool]:
        return self._values.get('terminate_instances_with_expiration')

    @builtins.property
    def valid_from(self) -> typing.Optional[str]:
        return self._values.get('valid_from')

    @builtins.property
    def valid_until(self) -> typing.Optional[str]:
        return self._values.get('valid_until')

    @builtins.property
    def cluster(self) -> "EksSpotCluster":
        return self._values.get('cluster')

    @builtins.property
    def launch_template(self) -> typing.Optional["ILaunchtemplate"]:
        return self._values.get('launch_template')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'SpotFleetProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


__all__ = [
    "BaseSpotFleetProps",
    "BlockDuration",
    "ClusterVersion",
    "EksSpotCluster",
    "EksSpotClusterProps",
    "ILaunchtemplate",
    "InstanceInterruptionBehavior",
    "LaunchTemplate",
    "SpotFleet",
    "SpotFleetLaunchTemplateConfig",
    "SpotFleetProps",
]

publication.publish()
