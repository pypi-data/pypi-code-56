import responses
import requests
from unittest.mock import Mock

from cpaassdk.utils import (
  build_error_response,
  convert_to_dict,
  id_from,
  outer_dict_value,
  process_response,
  remove_empty_from_dict
)
from tests.util import deep_equal

class ResponseMocker:
  def __init__(self):
    self.base_url = 'https://random-base-url.com'
    self.test_url = self.base_url + '/test'

  def mock_request(self, req_type = 'test', status_code = 200):
    req_body = None

    if req_type == 'test':
      req_body = {
        '__for_test__': {
          'KeyOne': 'ValueOne'
        }
      }
    elif req_type == 'error':
      req_body =  {
        'requestError': {
          'serviceException': {
            'messageId': 'test-exception-id',
            'text': 'Attribute %1 specified in message part %2 is a duplicate',
            'variables': [
              'john',
              'userName'
            ]
          }
        }
      }
    elif req_type == 'success':
      req_body =  {
        'resourceURL': 'some/random/test/url/test-code-id'
      }

    responses.add(responses.GET, self.test_url, json=req_body, status=status_code)

  def send_mock_request(self):
    return requests.get(self.test_url)

class TestUtil:
  def test_remove_empty_from_dict(self):
    input = {
      'key-1': 10,
      'key-2': 20,
      'key-3': None,
      'key-4': ''
    }

    expected_output = {
      'key-1': 10,
      'key-2': 20
    }

    output = remove_empty_from_dict(input)

    assert deep_equal(output, expected_output)

  def test_build_error_response_with_message_id(self):
    input = {
      'request_error': {
        'service_exception': {
          'message_id': 'test-exception-id',
          'text': 'Attribute %1 specified in message part %2 is a duplicate',
          'variables': [
            'john',
            'userName'
          ]
        }
      }
    }

    expected_output = {
      'name': 'service_exception',
      'exception_id': 'test-exception-id',
      'message': 'Attribute john specified in message part userName is a duplicate'
    }

    output = build_error_response(input)

    assert deep_equal(output, expected_output)

  def test_build_error_response_without_message_id(self):
    input = {
      'message': 'Some error message'
    }

    expected_output = {
      'name': 'request_error',
      'exception_id': 'unknown',
      'message': 'Some error message'
    }

    output = build_error_response(input)

    assert deep_equal(output, expected_output)

  def test_build_error_response_with_error_description(self):
    input = {
      'error': 'error',
      'error_description': 'Some error message'
    }

    expected_output = {
      'name': 'request_error',
      'exception_id': 'error',
      'message': 'Some error message'
    }

    output = build_error_response(input)

    assert deep_equal(output, expected_output)

  def test_build_error_response_with_empty_dict(self):
    input = {}

    expected_output = {
      'name': 'request_error',
      'exception_id': 'unknown',
      'message': '<no response>'
    }

    output = build_error_response(input)

    assert deep_equal(output, expected_output)

  def test_outer_dict_value(self):
    input = {
      'parent': {
        'child': {
          'grandchild': {
            'value': 10
          }
        }
      }
    }

    expected_output = {
      'child': {
        'grandchild': {
          'value': 10
        }
      }
    }

    output = outer_dict_value(input)

    assert deep_equal(output, expected_output)

  def test_id_from(self):
    input = '/some/url/test-id'

    expected_output = 'test-id'

    output = id_from(input)

    assert expected_output == output

  @responses.activate
  def test_process_response_with_test_response(self):
    response_mocker = ResponseMocker()
    response_mocker.mock_request()
    input = response_mocker.send_mock_request()
    print(input)
    expected_output = {
      '__for_test__': {
        'key_one': 'ValueOne'
      }
    }

    output = process_response(input)
    print(output)
    assert expected_output == output

  @responses.activate
  def test_process_response_with_error_response(self):
    response_mocker = ResponseMocker()
    response_mocker.mock_request(status_code = 401, req_type = 'error')
    input = response_mocker.send_mock_request()

    expected_output = {
      'name': 'service_exception',
      'exception_id': 'test-exception-id',
      'message': 'Attribute john specified in message part userName is a duplicate'
    }

    output = process_response(input)
    assert expected_output == output

  @responses.activate
  def test_process_response_with_normal_response_without_callback(self):
    response_mocker = ResponseMocker()
    response_mocker.mock_request(req_type = 'success')
    input = response_mocker.send_mock_request()

    expected_output = {
      'resourceurl': 'some/random/test/url/test-code-id'
    }

    output = process_response(input)

    assert expected_output == output

  @responses.activate
  def test_process_response_with_normal_response_with_callback(self):
    response_mocker = ResponseMocker()
    response_mocker.mock_request(req_type = 'success')
    input = response_mocker.send_mock_request()

    callback_input = {
      'resourceurl': 'some/random/test/url/test-code-id'
    }

    func = Mock()

    output = process_response(input, callback=func)

    func.assert_called_with(callback_input)

  @responses.activate
  def test_process_response_with_empty_response_with_callback(self):
    response_mocker = ResponseMocker()
    response_mocker.mock_request(req_type = 'empty')
    input = response_mocker.send_mock_request()

    callback_input = {}

    func = Mock()

    output = process_response(input, callback=func)

    func.assert_called_with(callback_input)

  @responses.activate
  def test_process_response_with_empty_response_without_callback(self):
    response_mocker = ResponseMocker()
    response_mocker.mock_request(req_type = 'empty')
    input = response_mocker.send_mock_request()

    callback_input = {}
    expected_output = {}

    func = Mock()

    output = process_response(input)

    func.assert_not_called()
    assert output == {}

  @responses.activate
  def test_convert_to_dict_with_valid_input(self):
    response_mocker = ResponseMocker()
    response_mocker.mock_request(req_type = 'success')
    input = response_mocker.send_mock_request()

    expected_output = {
      'resourceurl': 'some/random/test/url/test-code-id'
    }
    output = convert_to_dict(input)
    assert expected_output == output

  @responses.activate
  def test_convert_to_dict_with_empty_input(self):
    response_mocker = ResponseMocker()
    response_mocker.mock_request(req_type = 'empty')
    input = response_mocker.send_mock_request()

    expected_output = {}

    output = convert_to_dict(input)
    assert expected_output == output

  def test_convert_to_dict_with_invalid_input(self):
    expected_output = {}

    output = convert_to_dict(None)
    assert expected_output == output
