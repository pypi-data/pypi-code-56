import os

def isLambda():
    return os.getenv('_HANDLER', None) is not None

def init(api):
    import bootstrap

    old_handle_request = bootstrap.handle_event_request
    def _newHandleRequest(lambda_runtime_client, request_handler, *args):
        def _newRequestHandler(event, context):
            task_input = event

            task = api.createTask(
                context.function_name, 
                context.aws_request_id, 
                task_input=task_input,
                task_metadata=dict(
                    logGroupName=context.log_group_name,
                    logStreamName=context.log_stream_name,
                    region=os.getenv('AWS_REGION', None)
                )
            )

            try:
                task_output = request_handler(event, context)
            except Exception as e:
                task.update(task_status='failed', task_output=str(e))
                raise e

            task.update(task_status='succeeded', task_output=task_output)
            return task_output

        old_handle_request(lambda_runtime_client, _newRequestHandler, *args)
    bootstrap.handle_event_request = _newHandleRequest
