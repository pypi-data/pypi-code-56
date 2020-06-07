import os

import requests

from dagger.constants import DAGGER_URL
from dagger.Task import TaskListener, Task

class DaggerAPI(TaskListener):
    def __init__(self, api_token):
        self.api_token = api_token

    def createTask(self, task_name, task_run_id, initial_status='started', **update_kwargs):
        return Task(self, task_name, task_run_id).update(task_status=initial_status, **update_kwargs)

    def sendTaskStatus(self, status, task_name, task_run_id, task_input, task_output, task_metadata):
        body = dict(
            status=status,
            task_name=task_name,
            id=task_run_id,
            input=dict(input=task_input),
            output=dict(output=task_output),
            metadata=task_metadata,
            api_token=self.api_token
        )

        response = requests.post(
            DAGGER_URL,
            json=body
        )

    def onTaskUpdate(self, task):
        self.sendTaskStatus(
            task.task_status,
            task.task_name,
            task.task_run_id,
            task.task_input,
            task.task_output,
            task.task_metadata
        )
