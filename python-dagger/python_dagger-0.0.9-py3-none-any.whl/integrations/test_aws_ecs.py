import os
import unittest
from unittest.mock import patch, MagicMock

from dagger.integrations.aws_ecs import wrapMainFunction

TEST_EXECUTION_ENV = {
    'DockerId': 'docker-id',
    'Name': 'container-name', 
    'DockerName': 'docker-name', 
    'Image': 'docker-image', 
    'ImageID': 'image-id', 
    'Labels': {
        'com.amazonaws.ecs.cluster': 'test-cluster', 
        'com.amazonaws.ecs.container-name': 'test-container-name', 
        'com.amazonaws.ecs.task-arn': 'test-task-arn/1234', 
        'com.amazonaws.ecs.task-definition-family': 'test-task-definition-family', 
        'com.amazonaws.ecs.task-definition-version': 'test-task-definition-version'
    },
    'DesiredStatus': 'RUNNING', 
    'KnownStatus': 'RUNNING', 
    'Limits': {'CPU': 0, 'Memory': 2048}, 
    'CreatedAt': '2020-06-07T16:07:45.321115096Z', 
    'StartedAt': '2020-06-07T16:08:10.522444681Z', 
    'Type': 'NORMAL', 
    'Networks': [{'NetworkMode': 'awsvpc', 'IPv4Addresses': ['10.0.21.154']}]
}

def mock_requests(url):
    mock_response = MagicMock()
    mock_response.json.return_value = TEST_EXECUTION_ENV
    return mock_response

@patch('dagger.integrations.aws_ecs.requests.get', side_effect=mock_requests)
class TestAWSECSIntegration(unittest.TestCase):
    def tearDown(self):
        remove_env_variables = ['AWS_REGION', 'ECS_CONTAINER_METADATA_URI']
        for env_variable_name in remove_env_variables:
            if env_variable_name in os.environ:
                del os.environ[env_variable_name]

    @patch('dagger.integrations.aws_ecs.__main__')
    def test_wrapFunction(self, mock_main, mock_request_get):
        mock_main.__file__ = 'test'

        mock_dagger_api = MagicMock()
        mock_main_func = MagicMock()

        wrapped_func = wrapMainFunction(mock_dagger_api, mock_main_func)

        mock_input = MagicMock()
        wrapped_func(mock_input, asdf=mock_input)

        mock_main_func.assert_called_with(mock_input, asdf=mock_input)

        mock_dagger_api.createTask.assert_called_with(
            mock_main.__file__, 
            TEST_EXECUTION_ENV['Labels']['com.amazonaws.ecs.task-arn'], 
            task_input={
                'args': (mock_input, ), 
                'kwargs': {'asdf': mock_input}
            },
            task_metadata={
                'region': None,
                'execution_env': None,
                'logGroupName': '/ecs/test-task-definition-family',
                'logStreamName': 'ecs/test-container-name/1234',
                'ecs_container_metadata': TEST_EXECUTION_ENV
            }
        )
