from unittest import TestCase
from only_utils.utils.classes import Response


class TestResponse(TestCase):

    def test_ok(self):
        result = Response(
            http_code=200,
            message='OK',
            data={}
        )
        expected = {
            'http_code': 200,
            'message': 'OK',
            'error': None,
            'data': {}
            }
        self.assertEqual(result.__json__(), expected)
        self.assertIsInstance(result, Response)

    def test_not_data(self):
        result = Response()
        expected = {
            'http_code': None,
            'message': None,
            'error': None,
            'data': None
            }
        self.assertEqual(result.__json__(), expected)
        self.assertIsInstance(result, Response)
