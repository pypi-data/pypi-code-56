import unittest
import json
from fixtures.app import app


class TestRequestParsing(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_get_request_body_validated(self):
        resp = self.client.get("/test_get_request_body_validated")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.content_type, "application/json")

    def test_ok_valid(self):
        payload_ok = {
            "destination": ["email@test.com"],
            "message": "testing the validation of json request."
        }
        resp = self.client.post("/test_ok_valid", data=json.dumps(payload_ok), content_type="application/json")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.content_type, "application/json")
        self.assertEqual(resp.json['state'], 'sent')

    def test_ok_bad_request_missing_required(self):
        payload_bad_request = {
            "not_destination": ["email@test.com"],
            "message": "testing the validation of json request."
        }
        resp = self.client.post(
            "/test_ok_valid",
            data=json.dumps(payload_bad_request),
            content_type="application/json",
        )
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp.content_type, "application/json")
        self.assertEqual(resp.json['message'], "'destination' is a required property")

    def test_ok_bad_request_invalid_value(self):
        payload_bad_request = {
            "destination": ["test"],
            "message": "testing the validation of json request."
        }
        resp = self.client.post(
            "/test_ok_valid",
            data=json.dumps(payload_bad_request),
            content_type="application/json",
        )
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp.content_type, "application/json")
        self.assertEqual(resp.json['message'], "'test' is not a 'email'")
        self.assertEqual(resp.json['invalid'], ['destination', 0])




if __name__ == '__main__':
    unittest.main()
