"""
[![npm version](https://badge.fury.io/js/aws-lambda-golang.svg)](https://badge.fury.io/js/aws-lambda-golang)

## Amazon Lambda Golang Construct

This library provides constructs for Golang (Go 1.11 and 1.12 because of go modules) Lambda functions.

### Golang Function

Define a `GolangFunction`:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
lambda.GolangFunction(self, "my-handler")
```

By default, the construct will use the name of the defining file and the construct's id to look
up the entry file:

```
.
├── stack.ts # defines a 'GolangFunction' with 'my-handler' as id
├── stack/my-handler/main.go
├── stack/my-handler/go.mod
├── stack/my-handler/go.sum
```

### Configuring build

The `GolangFunction` construct exposes some options via properties: `buildCmd`, `buildDir`, `entry` and `handler`, `extraEnv`.

By default, your Golang code is compiled using `go build -ldflags="-s -w"` command with `GOOS=linux` env variable.

Project sponsored by [Dynobase](https://dynobase.dev)
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

import aws_cdk.aws_ec2
import aws_cdk.aws_iam
import aws_cdk.aws_lambda
import aws_cdk.aws_logs
import aws_cdk.aws_sqs
import aws_cdk.core


class GolangFunction(aws_cdk.aws_lambda.Function, metaclass=jsii.JSIIMeta, jsii_type="aws-lambda-golang.GolangFunction"):
    """A Node.js Lambda function bundled using Parcel.

    stability
    :stability: experimental
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, build_cmd: typing.Optional[str]=None, build_dir: typing.Optional[str]=None, entry: typing.Optional[str]=None, extra_env: typing.Any=None, handler: typing.Optional[str]=None, allow_all_outbound: typing.Optional[bool]=None, current_version_options: typing.Optional[aws_cdk.aws_lambda.VersionOptions]=None, dead_letter_queue: typing.Optional[aws_cdk.aws_sqs.IQueue]=None, dead_letter_queue_enabled: typing.Optional[bool]=None, description: typing.Optional[str]=None, environment: typing.Optional[typing.Mapping[str, str]]=None, events: typing.Optional[typing.List[aws_cdk.aws_lambda.IEventSource]]=None, function_name: typing.Optional[str]=None, initial_policy: typing.Optional[typing.List[aws_cdk.aws_iam.PolicyStatement]]=None, layers: typing.Optional[typing.List[aws_cdk.aws_lambda.ILayerVersion]]=None, log_retention: typing.Optional[aws_cdk.aws_logs.RetentionDays]=None, log_retention_role: typing.Optional[aws_cdk.aws_iam.IRole]=None, memory_size: typing.Optional[jsii.Number]=None, reserved_concurrent_executions: typing.Optional[jsii.Number]=None, role: typing.Optional[aws_cdk.aws_iam.IRole]=None, security_group: typing.Optional[aws_cdk.aws_ec2.ISecurityGroup]=None, security_groups: typing.Optional[typing.List[aws_cdk.aws_ec2.ISecurityGroup]]=None, timeout: typing.Optional[aws_cdk.core.Duration]=None, tracing: typing.Optional[aws_cdk.aws_lambda.Tracing]=None, vpc: typing.Optional[aws_cdk.aws_ec2.IVpc]=None, vpc_subnets: typing.Optional[aws_cdk.aws_ec2.SubnetSelection]=None, max_event_age: typing.Optional[aws_cdk.core.Duration]=None, on_failure: typing.Optional[aws_cdk.aws_lambda.IDestination]=None, on_success: typing.Optional[aws_cdk.aws_lambda.IDestination]=None, retry_attempts: typing.Optional[jsii.Number]=None) -> None:
        """
        :param scope: -
        :param id: -
        :param build_cmd: The build command. Default: - ``go build -ldflags="-s -w"``
        :param build_dir: The build directory. Default: - ``.build`` in the entry file directory
        :param entry: Path to the entry Golang source file. Default: - Derived from the name of the defining file and the construct's id. If the ``GolangFunction`` is defined in ``stack.ts`` with ``my-handler`` as id (``new GolangFunction(this, 'my-handler')``), the construct will look at ``stack/my-handler/main.go``
        :param extra_env: Additional environment variables. Default: - ``{ GOOS: 'linux' }``
        :param handler: The name of the exported handler in the entry file. Default: main
        :param allow_all_outbound: Whether to allow the Lambda to send all network traffic. If set to false, you must individually add traffic rules to allow the Lambda to connect to network targets. Default: true
        :param current_version_options: Options for the ``lambda.Version`` resource automatically created by the ``fn.currentVersion`` method. Default: - default options as described in ``VersionOptions``
        :param dead_letter_queue: The SQS queue to use if DLQ is enabled. Default: - SQS queue with 14 day retention period if ``deadLetterQueueEnabled`` is ``true``
        :param dead_letter_queue_enabled: Enabled DLQ. If ``deadLetterQueue`` is undefined, an SQS queue with default options will be defined for your Function. Default: - false unless ``deadLetterQueue`` is set, which implies DLQ is enabled.
        :param description: A description of the function. Default: - No description.
        :param environment: Key-value pairs that Lambda caches and makes available for your Lambda functions. Use environment variables to apply configuration changes, such as test and production environment configurations, without changing your Lambda function source code. Default: - No environment variables.
        :param events: Event sources for this function. You can also add event sources using ``addEventSource``. Default: - No event sources.
        :param function_name: A name for the function. Default: - AWS CloudFormation generates a unique physical ID and uses that ID for the function's name. For more information, see Name Type.
        :param initial_policy: Initial policy statements to add to the created Lambda Role. You can call ``addToRolePolicy`` to the created lambda to add statements post creation. Default: - No policy statements are added to the created Lambda role.
        :param layers: A list of layers to add to the function's execution environment. You can configure your Lambda function to pull in additional code during initialization in the form of layers. Layers are packages of libraries or other dependencies that can be used by mulitple functions. Default: - No layers.
        :param log_retention: The number of days log events are kept in CloudWatch Logs. When updating this property, unsetting it doesn't remove the log retention policy. To remove the retention policy, set the value to ``INFINITE``. Default: logs.RetentionDays.INFINITE
        :param log_retention_role: The IAM role for the Lambda function associated with the custom resource that sets the retention policy. Default: - A new role is created.
        :param memory_size: The amount of memory, in MB, that is allocated to your Lambda function. Lambda uses this value to proportionally allocate the amount of CPU power. For more information, see Resource Model in the AWS Lambda Developer Guide. Default: 128
        :param reserved_concurrent_executions: The maximum of concurrent executions you want to reserve for the function. Default: - No specific limit - account limit.
        :param role: Lambda execution role. This is the role that will be assumed by the function upon execution. It controls the permissions that the function will have. The Role must be assumable by the 'lambda.amazonaws.com' service principal. The default Role automatically has permissions granted for Lambda execution. If you provide a Role, you must add the relevant AWS managed policies yourself. The relevant managed policies are "service-role/AWSLambdaBasicExecutionRole" and "service-role/AWSLambdaVPCAccessExecutionRole". Default: - A unique role will be generated for this lambda function. Both supplied and generated roles can always be changed by calling ``addToRolePolicy``.
        :param security_group: What security group to associate with the Lambda's network interfaces. This property is being deprecated, consider using securityGroups instead. Only used if 'vpc' is supplied. Use securityGroups property instead. Function constructor will throw an error if both are specified. Default: - If the function is placed within a VPC and a security group is not specified, either by this or securityGroups prop, a dedicated security group will be created for this function.
        :param security_groups: The list of security groups to associate with the Lambda's network interfaces. Only used if 'vpc' is supplied. Default: - If the function is placed within a VPC and a security group is not specified, either by this or securityGroup prop, a dedicated security group will be created for this function.
        :param timeout: The function execution time (in seconds) after which Lambda terminates the function. Because the execution time affects cost, set this value based on the function's expected execution time. Default: Duration.seconds(3)
        :param tracing: Enable AWS X-Ray Tracing for Lambda Function. Default: Tracing.Disabled
        :param vpc: VPC network to place Lambda network interfaces. Specify this if the Lambda function needs to access resources in a VPC. Default: - Function is not placed within a VPC.
        :param vpc_subnets: Where to place the network interfaces within the VPC. Only used if 'vpc' is supplied. Note: internet access for Lambdas requires a NAT gateway, so picking Public subnets is not allowed. Default: - the Vpc default strategy if not specified
        :param max_event_age: The maximum age of a request that Lambda sends to a function for processing. Minimum: 60 seconds Maximum: 6 hours Default: Duration.hours(6)
        :param on_failure: The destination for failed invocations. Default: - no destination
        :param on_success: The destination for successful invocations. Default: - no destination
        :param retry_attempts: The maximum number of times to retry when the function returns an error. Minimum: 0 Maximum: 2 Default: 2

        stability
        :stability: experimental
        """
        props = GolangFunctionProps(build_cmd=build_cmd, build_dir=build_dir, entry=entry, extra_env=extra_env, handler=handler, allow_all_outbound=allow_all_outbound, current_version_options=current_version_options, dead_letter_queue=dead_letter_queue, dead_letter_queue_enabled=dead_letter_queue_enabled, description=description, environment=environment, events=events, function_name=function_name, initial_policy=initial_policy, layers=layers, log_retention=log_retention, log_retention_role=log_retention_role, memory_size=memory_size, reserved_concurrent_executions=reserved_concurrent_executions, role=role, security_group=security_group, security_groups=security_groups, timeout=timeout, tracing=tracing, vpc=vpc, vpc_subnets=vpc_subnets, max_event_age=max_event_age, on_failure=on_failure, on_success=on_success, retry_attempts=retry_attempts)

        jsii.create(GolangFunction, self, [scope, id, props])


@jsii.data_type(jsii_type="aws-lambda-golang.GolangFunctionProps", jsii_struct_bases=[aws_cdk.aws_lambda.FunctionOptions], name_mapping={'max_event_age': 'maxEventAge', 'on_failure': 'onFailure', 'on_success': 'onSuccess', 'retry_attempts': 'retryAttempts', 'allow_all_outbound': 'allowAllOutbound', 'current_version_options': 'currentVersionOptions', 'dead_letter_queue': 'deadLetterQueue', 'dead_letter_queue_enabled': 'deadLetterQueueEnabled', 'description': 'description', 'environment': 'environment', 'events': 'events', 'function_name': 'functionName', 'initial_policy': 'initialPolicy', 'layers': 'layers', 'log_retention': 'logRetention', 'log_retention_role': 'logRetentionRole', 'memory_size': 'memorySize', 'reserved_concurrent_executions': 'reservedConcurrentExecutions', 'role': 'role', 'security_group': 'securityGroup', 'security_groups': 'securityGroups', 'timeout': 'timeout', 'tracing': 'tracing', 'vpc': 'vpc', 'vpc_subnets': 'vpcSubnets', 'build_cmd': 'buildCmd', 'build_dir': 'buildDir', 'entry': 'entry', 'extra_env': 'extraEnv', 'handler': 'handler'})
class GolangFunctionProps(aws_cdk.aws_lambda.FunctionOptions):
    def __init__(self, *, max_event_age: typing.Optional[aws_cdk.core.Duration]=None, on_failure: typing.Optional[aws_cdk.aws_lambda.IDestination]=None, on_success: typing.Optional[aws_cdk.aws_lambda.IDestination]=None, retry_attempts: typing.Optional[jsii.Number]=None, allow_all_outbound: typing.Optional[bool]=None, current_version_options: typing.Optional[aws_cdk.aws_lambda.VersionOptions]=None, dead_letter_queue: typing.Optional[aws_cdk.aws_sqs.IQueue]=None, dead_letter_queue_enabled: typing.Optional[bool]=None, description: typing.Optional[str]=None, environment: typing.Optional[typing.Mapping[str, str]]=None, events: typing.Optional[typing.List[aws_cdk.aws_lambda.IEventSource]]=None, function_name: typing.Optional[str]=None, initial_policy: typing.Optional[typing.List[aws_cdk.aws_iam.PolicyStatement]]=None, layers: typing.Optional[typing.List[aws_cdk.aws_lambda.ILayerVersion]]=None, log_retention: typing.Optional[aws_cdk.aws_logs.RetentionDays]=None, log_retention_role: typing.Optional[aws_cdk.aws_iam.IRole]=None, memory_size: typing.Optional[jsii.Number]=None, reserved_concurrent_executions: typing.Optional[jsii.Number]=None, role: typing.Optional[aws_cdk.aws_iam.IRole]=None, security_group: typing.Optional[aws_cdk.aws_ec2.ISecurityGroup]=None, security_groups: typing.Optional[typing.List[aws_cdk.aws_ec2.ISecurityGroup]]=None, timeout: typing.Optional[aws_cdk.core.Duration]=None, tracing: typing.Optional[aws_cdk.aws_lambda.Tracing]=None, vpc: typing.Optional[aws_cdk.aws_ec2.IVpc]=None, vpc_subnets: typing.Optional[aws_cdk.aws_ec2.SubnetSelection]=None, build_cmd: typing.Optional[str]=None, build_dir: typing.Optional[str]=None, entry: typing.Optional[str]=None, extra_env: typing.Any=None, handler: typing.Optional[str]=None) -> None:
        """Properties for a GolangFunction.

        :param max_event_age: The maximum age of a request that Lambda sends to a function for processing. Minimum: 60 seconds Maximum: 6 hours Default: Duration.hours(6)
        :param on_failure: The destination for failed invocations. Default: - no destination
        :param on_success: The destination for successful invocations. Default: - no destination
        :param retry_attempts: The maximum number of times to retry when the function returns an error. Minimum: 0 Maximum: 2 Default: 2
        :param allow_all_outbound: Whether to allow the Lambda to send all network traffic. If set to false, you must individually add traffic rules to allow the Lambda to connect to network targets. Default: true
        :param current_version_options: Options for the ``lambda.Version`` resource automatically created by the ``fn.currentVersion`` method. Default: - default options as described in ``VersionOptions``
        :param dead_letter_queue: The SQS queue to use if DLQ is enabled. Default: - SQS queue with 14 day retention period if ``deadLetterQueueEnabled`` is ``true``
        :param dead_letter_queue_enabled: Enabled DLQ. If ``deadLetterQueue`` is undefined, an SQS queue with default options will be defined for your Function. Default: - false unless ``deadLetterQueue`` is set, which implies DLQ is enabled.
        :param description: A description of the function. Default: - No description.
        :param environment: Key-value pairs that Lambda caches and makes available for your Lambda functions. Use environment variables to apply configuration changes, such as test and production environment configurations, without changing your Lambda function source code. Default: - No environment variables.
        :param events: Event sources for this function. You can also add event sources using ``addEventSource``. Default: - No event sources.
        :param function_name: A name for the function. Default: - AWS CloudFormation generates a unique physical ID and uses that ID for the function's name. For more information, see Name Type.
        :param initial_policy: Initial policy statements to add to the created Lambda Role. You can call ``addToRolePolicy`` to the created lambda to add statements post creation. Default: - No policy statements are added to the created Lambda role.
        :param layers: A list of layers to add to the function's execution environment. You can configure your Lambda function to pull in additional code during initialization in the form of layers. Layers are packages of libraries or other dependencies that can be used by mulitple functions. Default: - No layers.
        :param log_retention: The number of days log events are kept in CloudWatch Logs. When updating this property, unsetting it doesn't remove the log retention policy. To remove the retention policy, set the value to ``INFINITE``. Default: logs.RetentionDays.INFINITE
        :param log_retention_role: The IAM role for the Lambda function associated with the custom resource that sets the retention policy. Default: - A new role is created.
        :param memory_size: The amount of memory, in MB, that is allocated to your Lambda function. Lambda uses this value to proportionally allocate the amount of CPU power. For more information, see Resource Model in the AWS Lambda Developer Guide. Default: 128
        :param reserved_concurrent_executions: The maximum of concurrent executions you want to reserve for the function. Default: - No specific limit - account limit.
        :param role: Lambda execution role. This is the role that will be assumed by the function upon execution. It controls the permissions that the function will have. The Role must be assumable by the 'lambda.amazonaws.com' service principal. The default Role automatically has permissions granted for Lambda execution. If you provide a Role, you must add the relevant AWS managed policies yourself. The relevant managed policies are "service-role/AWSLambdaBasicExecutionRole" and "service-role/AWSLambdaVPCAccessExecutionRole". Default: - A unique role will be generated for this lambda function. Both supplied and generated roles can always be changed by calling ``addToRolePolicy``.
        :param security_group: What security group to associate with the Lambda's network interfaces. This property is being deprecated, consider using securityGroups instead. Only used if 'vpc' is supplied. Use securityGroups property instead. Function constructor will throw an error if both are specified. Default: - If the function is placed within a VPC and a security group is not specified, either by this or securityGroups prop, a dedicated security group will be created for this function.
        :param security_groups: The list of security groups to associate with the Lambda's network interfaces. Only used if 'vpc' is supplied. Default: - If the function is placed within a VPC and a security group is not specified, either by this or securityGroup prop, a dedicated security group will be created for this function.
        :param timeout: The function execution time (in seconds) after which Lambda terminates the function. Because the execution time affects cost, set this value based on the function's expected execution time. Default: Duration.seconds(3)
        :param tracing: Enable AWS X-Ray Tracing for Lambda Function. Default: Tracing.Disabled
        :param vpc: VPC network to place Lambda network interfaces. Specify this if the Lambda function needs to access resources in a VPC. Default: - Function is not placed within a VPC.
        :param vpc_subnets: Where to place the network interfaces within the VPC. Only used if 'vpc' is supplied. Note: internet access for Lambdas requires a NAT gateway, so picking Public subnets is not allowed. Default: - the Vpc default strategy if not specified
        :param build_cmd: The build command. Default: - ``go build -ldflags="-s -w"``
        :param build_dir: The build directory. Default: - ``.build`` in the entry file directory
        :param entry: Path to the entry Golang source file. Default: - Derived from the name of the defining file and the construct's id. If the ``GolangFunction`` is defined in ``stack.ts`` with ``my-handler`` as id (``new GolangFunction(this, 'my-handler')``), the construct will look at ``stack/my-handler/main.go``
        :param extra_env: Additional environment variables. Default: - ``{ GOOS: 'linux' }``
        :param handler: The name of the exported handler in the entry file. Default: main

        stability
        :stability: experimental
        """
        if isinstance(current_version_options, dict): current_version_options = aws_cdk.aws_lambda.VersionOptions(**current_version_options)
        if isinstance(vpc_subnets, dict): vpc_subnets = aws_cdk.aws_ec2.SubnetSelection(**vpc_subnets)
        self._values = {
        }
        if max_event_age is not None: self._values["max_event_age"] = max_event_age
        if on_failure is not None: self._values["on_failure"] = on_failure
        if on_success is not None: self._values["on_success"] = on_success
        if retry_attempts is not None: self._values["retry_attempts"] = retry_attempts
        if allow_all_outbound is not None: self._values["allow_all_outbound"] = allow_all_outbound
        if current_version_options is not None: self._values["current_version_options"] = current_version_options
        if dead_letter_queue is not None: self._values["dead_letter_queue"] = dead_letter_queue
        if dead_letter_queue_enabled is not None: self._values["dead_letter_queue_enabled"] = dead_letter_queue_enabled
        if description is not None: self._values["description"] = description
        if environment is not None: self._values["environment"] = environment
        if events is not None: self._values["events"] = events
        if function_name is not None: self._values["function_name"] = function_name
        if initial_policy is not None: self._values["initial_policy"] = initial_policy
        if layers is not None: self._values["layers"] = layers
        if log_retention is not None: self._values["log_retention"] = log_retention
        if log_retention_role is not None: self._values["log_retention_role"] = log_retention_role
        if memory_size is not None: self._values["memory_size"] = memory_size
        if reserved_concurrent_executions is not None: self._values["reserved_concurrent_executions"] = reserved_concurrent_executions
        if role is not None: self._values["role"] = role
        if security_group is not None: self._values["security_group"] = security_group
        if security_groups is not None: self._values["security_groups"] = security_groups
        if timeout is not None: self._values["timeout"] = timeout
        if tracing is not None: self._values["tracing"] = tracing
        if vpc is not None: self._values["vpc"] = vpc
        if vpc_subnets is not None: self._values["vpc_subnets"] = vpc_subnets
        if build_cmd is not None: self._values["build_cmd"] = build_cmd
        if build_dir is not None: self._values["build_dir"] = build_dir
        if entry is not None: self._values["entry"] = entry
        if extra_env is not None: self._values["extra_env"] = extra_env
        if handler is not None: self._values["handler"] = handler

    @builtins.property
    def max_event_age(self) -> typing.Optional[aws_cdk.core.Duration]:
        """The maximum age of a request that Lambda sends to a function for processing.

        Minimum: 60 seconds
        Maximum: 6 hours

        default
        :default: Duration.hours(6)
        """
        return self._values.get('max_event_age')

    @builtins.property
    def on_failure(self) -> typing.Optional[aws_cdk.aws_lambda.IDestination]:
        """The destination for failed invocations.

        default
        :default: - no destination
        """
        return self._values.get('on_failure')

    @builtins.property
    def on_success(self) -> typing.Optional[aws_cdk.aws_lambda.IDestination]:
        """The destination for successful invocations.

        default
        :default: - no destination
        """
        return self._values.get('on_success')

    @builtins.property
    def retry_attempts(self) -> typing.Optional[jsii.Number]:
        """The maximum number of times to retry when the function returns an error.

        Minimum: 0
        Maximum: 2

        default
        :default: 2
        """
        return self._values.get('retry_attempts')

    @builtins.property
    def allow_all_outbound(self) -> typing.Optional[bool]:
        """Whether to allow the Lambda to send all network traffic.

        If set to false, you must individually add traffic rules to allow the
        Lambda to connect to network targets.

        default
        :default: true
        """
        return self._values.get('allow_all_outbound')

    @builtins.property
    def current_version_options(self) -> typing.Optional[aws_cdk.aws_lambda.VersionOptions]:
        """Options for the ``lambda.Version`` resource automatically created by the ``fn.currentVersion`` method.

        default
        :default: - default options as described in ``VersionOptions``
        """
        return self._values.get('current_version_options')

    @builtins.property
    def dead_letter_queue(self) -> typing.Optional[aws_cdk.aws_sqs.IQueue]:
        """The SQS queue to use if DLQ is enabled.

        default
        :default: - SQS queue with 14 day retention period if ``deadLetterQueueEnabled`` is ``true``
        """
        return self._values.get('dead_letter_queue')

    @builtins.property
    def dead_letter_queue_enabled(self) -> typing.Optional[bool]:
        """Enabled DLQ.

        If ``deadLetterQueue`` is undefined,
        an SQS queue with default options will be defined for your Function.

        default
        :default: - false unless ``deadLetterQueue`` is set, which implies DLQ is enabled.
        """
        return self._values.get('dead_letter_queue_enabled')

    @builtins.property
    def description(self) -> typing.Optional[str]:
        """A description of the function.

        default
        :default: - No description.
        """
        return self._values.get('description')

    @builtins.property
    def environment(self) -> typing.Optional[typing.Mapping[str, str]]:
        """Key-value pairs that Lambda caches and makes available for your Lambda functions.

        Use environment variables to apply configuration changes, such
        as test and production environment configurations, without changing your
        Lambda function source code.

        default
        :default: - No environment variables.
        """
        return self._values.get('environment')

    @builtins.property
    def events(self) -> typing.Optional[typing.List[aws_cdk.aws_lambda.IEventSource]]:
        """Event sources for this function.

        You can also add event sources using ``addEventSource``.

        default
        :default: - No event sources.
        """
        return self._values.get('events')

    @builtins.property
    def function_name(self) -> typing.Optional[str]:
        """A name for the function.

        default
        :default:

        - AWS CloudFormation generates a unique physical ID and uses that
          ID for the function's name. For more information, see Name Type.
        """
        return self._values.get('function_name')

    @builtins.property
    def initial_policy(self) -> typing.Optional[typing.List[aws_cdk.aws_iam.PolicyStatement]]:
        """Initial policy statements to add to the created Lambda Role.

        You can call ``addToRolePolicy`` to the created lambda to add statements post creation.

        default
        :default: - No policy statements are added to the created Lambda role.
        """
        return self._values.get('initial_policy')

    @builtins.property
    def layers(self) -> typing.Optional[typing.List[aws_cdk.aws_lambda.ILayerVersion]]:
        """A list of layers to add to the function's execution environment.

        You can configure your Lambda function to pull in
        additional code during initialization in the form of layers. Layers are packages of libraries or other dependencies
        that can be used by mulitple functions.

        default
        :default: - No layers.
        """
        return self._values.get('layers')

    @builtins.property
    def log_retention(self) -> typing.Optional[aws_cdk.aws_logs.RetentionDays]:
        """The number of days log events are kept in CloudWatch Logs.

        When updating
        this property, unsetting it doesn't remove the log retention policy. To
        remove the retention policy, set the value to ``INFINITE``.

        default
        :default: logs.RetentionDays.INFINITE
        """
        return self._values.get('log_retention')

    @builtins.property
    def log_retention_role(self) -> typing.Optional[aws_cdk.aws_iam.IRole]:
        """The IAM role for the Lambda function associated with the custom resource that sets the retention policy.

        default
        :default: - A new role is created.
        """
        return self._values.get('log_retention_role')

    @builtins.property
    def memory_size(self) -> typing.Optional[jsii.Number]:
        """The amount of memory, in MB, that is allocated to your Lambda function.

        Lambda uses this value to proportionally allocate the amount of CPU
        power. For more information, see Resource Model in the AWS Lambda
        Developer Guide.

        default
        :default: 128
        """
        return self._values.get('memory_size')

    @builtins.property
    def reserved_concurrent_executions(self) -> typing.Optional[jsii.Number]:
        """The maximum of concurrent executions you want to reserve for the function.

        default
        :default: - No specific limit - account limit.

        see
        :see: https://docs.aws.amazon.com/lambda/latest/dg/concurrent-executions.html
        """
        return self._values.get('reserved_concurrent_executions')

    @builtins.property
    def role(self) -> typing.Optional[aws_cdk.aws_iam.IRole]:
        """Lambda execution role.

        This is the role that will be assumed by the function upon execution.
        It controls the permissions that the function will have. The Role must
        be assumable by the 'lambda.amazonaws.com' service principal.

        The default Role automatically has permissions granted for Lambda execution. If you
        provide a Role, you must add the relevant AWS managed policies yourself.

        The relevant managed policies are "service-role/AWSLambdaBasicExecutionRole" and
        "service-role/AWSLambdaVPCAccessExecutionRole".

        default
        :default:

        - A unique role will be generated for this lambda function.
          Both supplied and generated roles can always be changed by calling ``addToRolePolicy``.
        """
        return self._values.get('role')

    @builtins.property
    def security_group(self) -> typing.Optional[aws_cdk.aws_ec2.ISecurityGroup]:
        """What security group to associate with the Lambda's network interfaces. This property is being deprecated, consider using securityGroups instead.

        Only used if 'vpc' is supplied.

        Use securityGroups property instead.
        Function constructor will throw an error if both are specified.

        default
        :default:

        - If the function is placed within a VPC and a security group is
          not specified, either by this or securityGroups prop, a dedicated security
          group will be created for this function.

        deprecated
        :deprecated: - This property is deprecated, use securityGroups instead

        stability
        :stability: deprecated
        """
        return self._values.get('security_group')

    @builtins.property
    def security_groups(self) -> typing.Optional[typing.List[aws_cdk.aws_ec2.ISecurityGroup]]:
        """The list of security groups to associate with the Lambda's network interfaces.

        Only used if 'vpc' is supplied.

        default
        :default:

        - If the function is placed within a VPC and a security group is
          not specified, either by this or securityGroup prop, a dedicated security
          group will be created for this function.
        """
        return self._values.get('security_groups')

    @builtins.property
    def timeout(self) -> typing.Optional[aws_cdk.core.Duration]:
        """The function execution time (in seconds) after which Lambda terminates the function.

        Because the execution time affects cost, set this value
        based on the function's expected execution time.

        default
        :default: Duration.seconds(3)
        """
        return self._values.get('timeout')

    @builtins.property
    def tracing(self) -> typing.Optional[aws_cdk.aws_lambda.Tracing]:
        """Enable AWS X-Ray Tracing for Lambda Function.

        default
        :default: Tracing.Disabled
        """
        return self._values.get('tracing')

    @builtins.property
    def vpc(self) -> typing.Optional[aws_cdk.aws_ec2.IVpc]:
        """VPC network to place Lambda network interfaces.

        Specify this if the Lambda function needs to access resources in a VPC.

        default
        :default: - Function is not placed within a VPC.
        """
        return self._values.get('vpc')

    @builtins.property
    def vpc_subnets(self) -> typing.Optional[aws_cdk.aws_ec2.SubnetSelection]:
        """Where to place the network interfaces within the VPC.

        Only used if 'vpc' is supplied. Note: internet access for Lambdas
        requires a NAT gateway, so picking Public subnets is not allowed.

        default
        :default: - the Vpc default strategy if not specified
        """
        return self._values.get('vpc_subnets')

    @builtins.property
    def build_cmd(self) -> typing.Optional[str]:
        """The build command.

        default
        :default: - ``go build -ldflags="-s -w"``

        stability
        :stability: experimental
        """
        return self._values.get('build_cmd')

    @builtins.property
    def build_dir(self) -> typing.Optional[str]:
        """The build directory.

        default
        :default: - ``.build`` in the entry file directory

        stability
        :stability: experimental
        """
        return self._values.get('build_dir')

    @builtins.property
    def entry(self) -> typing.Optional[str]:
        """Path to the entry Golang source file.

        default
        :default:

        - Derived from the name of the defining file and the construct's id.
          If the ``GolangFunction`` is defined in ``stack.ts`` with ``my-handler`` as id
          (``new GolangFunction(this, 'my-handler')``), the construct will look at ``stack/my-handler/main.go``

        stability
        :stability: experimental
        """
        return self._values.get('entry')

    @builtins.property
    def extra_env(self) -> typing.Any:
        """Additional environment variables.

        default
        :default: - ``{ GOOS: 'linux' }``

        stability
        :stability: experimental
        """
        return self._values.get('extra_env')

    @builtins.property
    def handler(self) -> typing.Optional[str]:
        """The name of the exported handler in the entry file.

        default
        :default: main

        stability
        :stability: experimental
        """
        return self._values.get('handler')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'GolangFunctionProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


__all__ = [
    "GolangFunction",
    "GolangFunctionProps",
]

publication.publish()
