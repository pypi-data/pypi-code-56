import sys
import json
import os

import requests

class DaggerAPI():
    def __init__(self, api_token):
        self.api_token = api_token

    def sendTaskStatus(self, status, context, task_input, task_output):
        body = dict(
            status=status,
            task_name=context.function_name,
            id=context.aws_request_id,
            input=task_input,
            output=dict(output=task_output),
            metadata=dict(
                logGroupName=context.log_group_name,
                logStreamName=context.log_stream_name,
                region=os.getenv('AWS_REGION', None)
            ),
            api_token=self.api_token
        )

        response = requests.post(
            'https://api.getdagger.com/v1/tasks/status',
            json=body
        )

        print(response, str(response.content))

def initLambda(api):
    import bootstrap

    old_handle_request = bootstrap.handle_event_request
    def _newHandleRequest(lambda_runtime_client, request_handler, *args):
        def _newRequestHandler(event, context):
            task_input = event
            api.sendTaskStatus('started', context, task_input, {})

            try:
                task_output = request_handler(event, context)
            except Exception as e:
                api.sendTaskStatus('failed', context, task_input, str(e))
                raise e

            api.sendTaskStatus('succeeded', context, task_input, task_output)
            return task_output

        old_handle_request(lambda_runtime_client, _newRequestHandler, *args)
    bootstrap.handle_event_request = _newHandleRequest


def initDagger(api_key):
    api = DaggerAPI(api_key)

    print(os.environ)

    if os.getenv('_HANDLER'):
        initLambda(api)

    return api
