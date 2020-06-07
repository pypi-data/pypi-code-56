import __main__
import os
import request

ENV_ECS_CONTAINER_METADATA_URI = 'ECS_CONTAINER_METADATA_URI'

def isECS():
    return os.environ(ENV_ECS_CONTAINER_METADATA_URI, None) is not None

def getTaskMetadataFromECS():
    res = requests.get(os.getenv('ECS_CONTAINER_METADATA_URI'))
    ecs_container_metadata = res.json()

    # TODO: There's no way this is stable:
    task_definition_family = ecs_container_metadata['Labels']['com.amazonaws.ecs.task-definition-family']
    container_name = ecs_container_metadata['Labels']['com.amazonaws.ecs.container-name']
    task_id = ecs_container_metadata['Labels']['com.amazonaws.ecs.task-arn'].split('/')[-1]

    log_group_name = '/ecs/' + task_definition_family
    log_stream_name = 'ecs/' + container_name + '/' + task_id

    return dict(
        logGroupName=log_group_name,
        logStreamName=log_stream_name,
        region=os.getenv('AWS_REGION', None),
        execution_env=os.getenv('AWS_EXECUTION_ENV', None),
        ecs_container_metadata=ecs_container_metadata
    )

def wrapMainFunction(dagger_api, func, task_name=None, task_run_id=None):
    if task_name is None:
        task_name = __main__.__file__

    def _wrapper(*args, **kwargs):
        task = None
        try:
            task_input = dict(
                args=*args,
                kwargs=**kwargs
            )

            task_metadata = dict(
                # logGroupName=context.log_group_name,
                # logStreamName=context.log_stream_name,
                region=os.getenv('AWS_REGION', None),
                execution_env=os.getenv('AWS_EXECUTION_ENV', None)
            )

            task = api.createTask(
                task_name,
                task_run_id,
                task_input=task_input,
                task_metadata=task_metadata
            )
        except Exception as e:
            print('Failed to initialize dagger')
            print(e)

        try:
            task_output = func(*args, **kwargs)
        except Exception as e:
            if task is not None:
                task.update(task_status='failed', task_output=str(e))

        try:
            task.update(task_status='succeeded', task_output=task_output)
        except Exception as e:
            print('Failed to log dagger output')
            print(e)

        return task_output

# {"function_version":"$LATEST","function_name":"complicated_job_rss","memoryLimitInMB":"512","logGroupName":"/aws/lambda/complicated_job_rss","logStreamName":"2020/05/24/[$LATEST]e47d9a855816499abffb1616ac6c1e9b","invokedFunctionArn":"arn:aws:lambda:us-east-2:985550760282:function:complicated_job_rss","awsRequestId":"00080e00-c853-469f-9ad8-57dca5c6c014"}
# {
#     'DockerId': 'd0e11205a44b5768cb03f9e160f2f4afb2b378d554974c42d018d262c2cfb7d8',
#     'Name': 'doralgo-l53-support', 
#     'DockerName': 'ecs-doralgo-l53-support-staging-3-doralgo-l53-support-a4df94f4ca8b88e1b101', 
#     'Image': '340301842845.dkr.ecr.us-west-2.amazonaws.com/doralgo-l53-support:staging', 
#     'ImageID': 'sha256:ab15381f4b91caeb9252181e2193d3d57099bd2c77161bbf22ce34960ade7ec2', 
#     'Labels': {'com.amazonaws.ecs.cluster': 'arn:aws:ecs:us-west-2:340301842845:cluster/doralgo', 'com.amazonaws.ecs.container-name': 'doralgo-l53-support', 'com.amazonaws.ecs.task-arn': 'arn:aws:ecs:us-west-2:340301842845:task/013a7a37-5e6f-4623-98ed-539340ef7711', 'com.amazonaws.ecs.task-definition-family': 'doralgo-l53-support-staging', 'com.amazonaws.ecs.task-definition-version': '3'}, 
#     'DesiredStatus': 'RUNNING', 
#     'KnownStatus': 'RUNNING', 
#     'Limits': {'CPU': 0, 'Memory': 2048}, 
#     'CreatedAt': '2020-06-07T16:07:45.321115096Z', 
#     'StartedAt': '2020-06-07T16:08:10.522444681Z', 
#     'Type': 'NORMAL', 
#     'Networks': [{'NetworkMode': 'awsvpc', 'IPv4Addresses': ['10.0.21.154']}]
# }